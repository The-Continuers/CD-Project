from transformers.sdt.stmts.expressions import Expression


class AccessExpression(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__()
        self.left, self.right = left, right
