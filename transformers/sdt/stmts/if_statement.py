from typing import List, TYPE_CHECKING, Optional

from transformers.sdt.stmts import Statement
from transformers.types import DecafBool

if TYPE_CHECKING:
    from transformers.sdt.stmts.expressions import Expression
    from code_generation import Context
    from transformers.sdt.stmts import StatementBlock


class IfStatement(Statement):
    def __init__(
            self, conditional_expr: "Expression",
            if_stmts: Optional["StatementBlock"],
            else_stmts: Optional["StatementBlock"],
    ):
        self.conditional_expr, self.if_stmts, self.else_stmts = conditional_expr, if_stmts, else_stmts
        # self.if_stmts.new_scope = False
        # if self.else_stmts is not None:
        #     self.else_stmts.new_scope = False

    def to_tac(self, context: "Context") -> List[str]:
        self.conditional_expr.type_checker.check_type(context=context, expected_type=DecafBool)

        if_codes = self.if_stmts.to_tac(context=context) if self.if_stmts else []
        else_codes = self.else_stmts.to_tac(
            context) if self.else_stmts else []
        end_if_label = context.get_end_if_else_label('if')
        end_else_label = context.get_end_if_else_label('else')
        return [
            '# if started',
            *self.conditional_expr.to_tac(context),
            f'beqz $t0, {end_if_label}',
            *if_codes,
            f'j {end_else_label}',
            f'{end_if_label}:',
            *else_codes,
            f'{end_else_label}:',
            '# if ended',
        ]
