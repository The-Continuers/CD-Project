from typing import List, TYPE_CHECKING

from transformers.sdt.stmts import Statement
from transformers.sdt.stmts.expressions import Expression

if TYPE_CHECKING:
    from code_generation import Context


class ReturnStatement(Statement):
    def __init__(self, return_expr: Expression):
        self.return_expr = return_expr

    def to_tac(self, context: "Context") -> List[str]:
        """
            if there exists a return value, it'll be stored in $t0 or $f0.
            therefore, after function return, the assign expression will use that $t0 or $f0,
            considering type-safety issues
        """
        codes = ["# return expression"]
        if self.return_expr is not None:
            codes += self.return_expr.to_tac(context=context)
        codes += [f'j end_function_{context.current_scope.get_name()} # Fuck Life']
        return codes
