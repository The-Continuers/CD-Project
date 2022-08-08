import operator
from typing import Callable, TYPE_CHECKING, List

from exceptions import CompilerPanic
from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafType, DecafInt, DecafDouble
from todos import Todo

if TYPE_CHECKING:
    from code_generation import Context


class BinaryExpression(Expression):
    # $t0: $t0 OP $t1
    @staticmethod
    def get_tac_code_op(op, context: "Context", data_type: DecafType = DecafInt) -> List[str]:
        def compare_code(op_str, boolean, label):
            return ['li $t0, 0', f'c.{op_str}.d $f0, $f2',
                    f'bc1{boolean} __label__{label}', 'li $t0, 1',
                    f'__label__{label}:']

        op_to_mips_op_int = {
            operator.or_: ['or $t0, $t0, $t1'],
            operator.and_: ['and $t0, $t0, $t1'],
            operator.eq: ['seq $t0, $t0, $t1'],
            operator.ne: ['sne $t0, $t0, $t1'],
            operator.lt: ['slt $t0, $t0, $t1'],
            operator.le: ['sle $t0, $t0, $t1'],
            operator.gt: ['sgt $t0, $t0, $t1'],
            operator.ge: ['sge $t0, $t0, $t1'],
            operator.add: ['add $t0, $t0, $t1'],
            operator.sub: ['sub $t0, $t0, $t1'],
            operator.mul: ['mul $t0, $t0, $t1'],
            operator.truediv: ['div $t0, $t0, $t1'],
            operator.mod: ['div $t0, $t1', 'mfhi $t0'],
        }
        label_name = context.current_scope.get_data_name(data_type)
        op_to_mips_op_double = {
            operator.or_: op_to_mips_op_int.get(operator.or_),
            operator.and_: op_to_mips_op_int.get(operator.and_),
            operator.eq: compare_code('eq', 'f', label_name),
            operator.ne: compare_code('eq', 't', label_name),
            operator.lt: compare_code('lt', 'f', label_name),
            operator.le: compare_code('le', 'f', label_name),
            operator.gt: compare_code('le', 't', label_name),
            operator.ge: compare_code('lt', 't', label_name),
            operator.add: ['add.d $f0, $f0, $f2'],
            operator.sub: ['sub.d $f0, $f0, $f2'],
            operator.mul: ['mul.d $f0, $f0, $f2'],
            operator.truediv: ['div.d $f0, $f0, $f2'],
        }
        if data_type == DecafDouble:
            return op_to_mips_op_double.get(op)
        return op_to_mips_op_int.get(op)

    def __init__(self, op: Callable, left: Expression, right: Expression) -> None:
        super().__init__()
        self.op, self.left, self.right = op, left, right

    def to_tac(self, context: "Context") -> List[str]:
        self.type_checker.check_type(context)
        l_type: DecafType = self.left.type_checker.check_type(context)
        # evaluate left
        codes = self.left.to_tac(context)
        # push evaluated left to stack
        codes += [
            "# push evaluated left to stack",
            *context.current_scope.push_to_stack(temp_t=l_type),
        ]
        # evaluate right
        codes += self.right.to_tac(context)
        # put evaluated right to $f1
        if l_type == DecafDouble:
            codes += [f"mov.d $f2, $f0  # move right evaluated to $f2"]
        else:
            codes += [f"move $t1, $t0 # move right evaluated to $t1"]
        # pop evaluated left from stack
        codes += [
            "# pop evaluated left from stack",
            *context.current_scope.pop_from_stack(temp_t=l_type)
        ]
        # put OP code to the operation
        codes += self.get_tac_code_op(op=self.op,
                                      context=context, data_type=l_type)
        return codes
