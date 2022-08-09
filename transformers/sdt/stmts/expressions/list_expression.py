from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafType


class ListExpression(Expression):
    def __init__(self, array_num_expr: Expression, array_type: DecafType) -> None:
        super().__init__()
        self.num_expr, self.type = array_num_expr, array_type
