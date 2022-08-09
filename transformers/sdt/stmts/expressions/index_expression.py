import operator
from typing import List, TYPE_CHECKING

from transformers.sdt.stmts.expressions import Expression, BinaryExpression, IntValue

if TYPE_CHECKING:
    from code_generation import Context
    from transformers.types import DecafArray, DecafDouble


class IndexExpression(Expression):
    def __init__(self, array: Expression, index: Expression) -> None:
        super().__init__()
        self.array, self.index = array, index

    def to_tac(self, context: "Context") -> List[str]:
        """
            Address Code: Array_Ref + Element_type_size * Index
        """
        array_type: "DecafArray" = self.array.type_checker.check_type(context=context)
        el_type_size: int = array_type.sub_type.size
        # Value Address Code
        codes = BinaryExpression(op=operator.add,
                                 left=self.array,
                                 right=BinaryExpression(op=operator.mul, left=IntValue(el_type_size),
                                                        right=self.index)).to_tac(context=context)
        # the result is in $t0
        codes += ["l.d $f0, $t0" if el_type_size == DecafDouble else "lw $t0, $t0"]
        return codes
