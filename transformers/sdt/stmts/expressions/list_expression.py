import operator
from typing import List, TYPE_CHECKING

from transformers.sdt.stmts.expressions import Expression, CallExpression, BinaryExpression, IntValue
from transformers.sdt.utils import VariableName
from transformers.types import DecafType

if TYPE_CHECKING:
    from code_generation import Context


class ListExpression(Expression):
    def __init__(self, array_num_expr: Expression, array_type: DecafType) -> None:
        super().__init__()
        self.num_expr, self.type = array_num_expr, array_type

    def to_tac(self, context: "Context") -> List[str]:
        """
        The Code is equivalent to "alloc(type_size * array_size)"
        """
        allocation_arg = BinaryExpression(op=operator.mul, left=self.num_expr, right=IntValue(self.type.size))
        return CallExpression(func_name=VariableName("alloc"), args=[allocation_arg]).to_tac(context=context)
