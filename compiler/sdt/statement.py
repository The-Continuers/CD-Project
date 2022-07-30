class Statement:
    pass


class Statements:
    pass


# todo
class Optional:
    pass


class IfStatement(Statement):
    def __init__(self, cond_expr, if_stmts, else_stmts) -> None:
        super().__init__()
        self.cond_expr = cond_expr
        self.if_stmts = if_stmts
        self.else_stmts = else_stmts


class WhileStatement(Statement):
    def __init__(self, cond_expr, while_stmts) -> None:
        super().__init__()
        self.cond_expr = cond_expr
        self.stmts = while_stmts


class ForStatement(Statement):
    def __init__(self, init_expr, iter_expr, post_expr, for_stmts) -> None:
        super().__init__()
        self.init_expr = init_expr
        self.iter_expr = iter_expr
        self.post_expr = post_expr
        self.stmts = for_stmts


class BreakStatement(Statement):
    def __init__(self) -> None:
        super().__init__()


class ContinueStatement(Statement):
    def __init__(self) -> None:
        super().__init__()


class ReturnStatement(Statement):
    def __init__(self, return_expr) -> None:
        super().__init__()
        self.expr = return_expr


class PrintStatement(Statement):
    def __init__(self, exprs) -> None:
        super().__init__()
        self.exprs = exprs
