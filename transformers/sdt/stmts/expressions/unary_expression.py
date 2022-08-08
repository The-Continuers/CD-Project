import operator
from typing import Callable, TYPE_CHECKING, List

from exceptions import CompilerPanic
from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafType, DecafInt, DecafDouble
from todos import Todo

if TYPE_CHECKING:
    from code_generation import Context


class UnaryExpression(Expression):
    @staticmethod
    def get_tac_code_op(op, context: "Context", data_type: DecafType = DecafInt) -> List[str]:
        op_to_mips_op_int = {
            operator.neg: ['sub $t0, $zero, $t0 # put 0-$t0 (neg $t0) in $t0'],
            operator.not_: ['li $t1, 1 # put 1 to $t1, because we dont have subi',
                            'sub $t0, $t1, $t0 # put 1-$t0 (not $t0) in $t0'],
        }
        op_to_mips_op_double = {
            operator.neg: ['sub.d $f2, $f2, $f2 # put 0 in $f2', 'sub.d $f0, $f2, $f0 # put 0-$f0 (neg $f0) in $f0'],
        }
        if data_type == DecafDouble:
            return op_to_mips_op_double.get(op)
        return op_to_mips_op_int.get(op)

    def __init__(self, op: Callable, operand: Expression) -> None:
        super().__init__()
        self.op, self.operand = op, operand

    def to_tac(self, context: "Context"):
        operand_type: "DecafType" = self.operand.type_checker.check_type(context=context)
        codes = self.operand.to_tac(context)
        codes += self.get_tac_code_op(op=self.op, context=context, data_type=operand_type)
        return codes
