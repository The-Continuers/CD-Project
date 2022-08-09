import operator
from typing import Callable, TYPE_CHECKING, List

from exceptions import CompilerPanic
from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafType, DecafInt, DecafDouble, DecafString

if TYPE_CHECKING:
    from code_generation import Context


def compare_code(op_str, boolean, label):
    return ['li $t0, 0', f'c.{op_str}.d $f0, $f2',
            f'bc1{boolean} __label__{label}', 'li $t0, 1',
            f'__label__{label}:']


class BinaryExpression(Expression):
    # $t0: $t0 OP $t1

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

    def get_tac_code_for_int_operation(self, context, data_type: DecafType) -> List[str]:
        return self.op_to_mips_op_int.get(self.op)

    def get_tac_code_for_double_operation(self, context, data_type: DecafType) -> List[str]:
        label_name = context.get_data_name(data_type)
        op_to_mips_op_double = {
            operator.or_: self.op_to_mips_op_int.get(operator.or_),
            operator.and_: self.op_to_mips_op_int.get(operator.and_),
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
        return op_to_mips_op_double.get(self.op)

    def get_tac_code_for_string_operation(self, context, data_type: DecafType) -> List[str]:
        codes = []
        if self.op in [operator.eq, operator.ne]:
            codes = [
                "# push string-equal inputs to stack",
                *context.current_scope.push_to_stack(temp_t=DecafInt),
                "move $t0, $t1 # move second arg in t0",
                *context.current_scope.push_to_stack(temp_t=DecafInt),
                'jal _StringEqual',
                'move $t0, $v0 # move string-equal return value in t0'
            ]
            if self.op == operator.ne:
                codes += [
                    'li $t1, 1 # put 1 to $t1, because we dont have subi',
                    'sub $t0, $t1, $t0 # put 1-$t0 (not $t0) in $t0'
                ]
        elif self.op == operator.add:
            context.add_data(
                data_name := context.get_data_name(data_type=DecafString),
                'space',
                1000
            )
            codes += [
                "# push string address 1 to stack",
                *context.current_scope.push_to_stack(temp_t=DecafInt),
                "move $t0, $t1 # move second arg in t0",
                "# push string address 2 to stack",
                *context.current_scope.push_to_stack(temp_t=DecafInt),
                f"la $t0, {data_name}\t# {data_name}'s address -> $t0"
                "# push string address result to stack",
                *context.current_scope.push_to_stack(temp_t=DecafInt),
                'jal _StringConcat'
            ]
        else:
            CompilerPanic('no other operation is supported for string values')
        return codes

    def get_tac_code_for_operation(self, context, data_type: DecafType) -> List[str]:
        return {
            DecafDouble: self.get_tac_code_for_double_operation,
            DecafString: self.get_tac_code_for_string_operation,
        }.get(data_type, self.get_tac_code_for_int_operation)(context, data_type)

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
        codes += self.get_tac_code_for_operation(context=context, data_type=l_type)
        return codes
