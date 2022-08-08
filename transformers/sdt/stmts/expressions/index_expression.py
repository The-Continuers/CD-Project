from transformers.sdt.stmts.expressions import Expression


class IndexExpression(Expression):
    def __init__(self, array: Expression, index: Expression) -> None:
        super().__init__()
        self.array, self.index = array, index
