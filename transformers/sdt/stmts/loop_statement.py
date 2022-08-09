from typing import TYPE_CHECKING, List, Optional

from code_generation import Context
from transformers.sdt.stmts import Statement, StatementBlock
from transformers.types import DecafDouble, DecafBool

if TYPE_CHECKING:
    from transformers.sdt.stmts.expressions import Expression


class WhileStatement(Statement):
    def __init__(self, cond_expr: 'Expression', stmts: StatementBlock) -> None:
        super().__init__()
        self.cond_expr = cond_expr
        self.stmts = stmts
        # self.stmts.new_scope = False
        self.end_label: Optional[str] = None
        self.continue_label: Optional[str] = None

    def before_codes_callback(self, context: "Context", codes: List[str]) -> None:
        pass

    def after_start_label_callback(self, context: "Context", codes: List[str]) -> None:
        pass

    def before_jump_callback(self, context: "Context", codes: List[str]) -> None:
        pass

    def to_tac(self, context: "Context") -> List[str]:
        self.cond_expr.type_checker.check_type(
            context, expected_type=DecafBool)
        with context.loop(self):
            codes = ['#loop started']
            end_label = f'end_{(start_label := context.get_loop_label())}'
            self.end_label = end_label
            self.before_codes_callback(context, codes)
            codes += [f"{start_label}:"]
            self.after_start_label_callback(context, codes)
            codes += self.cond_expr.to_tac(context)
            codes += [f"beqz $t0, {end_label}"]
            self.continue_label = f'cont_{start_label}'
            if self.stmts is not None:
                codes += self.stmts.to_tac(context)
            codes += [
                f'{self.continue_label}:'
            ]
            self.before_jump_callback(context, codes)
            codes += [
                f"j {start_label} # get back to start label",
                f"{end_label}:"
            ]
        codes += ['# loop ended']
        return codes


class ForStatement(WhileStatement):
    def __init__(
            self,
            init_expr: Optional['Expression'],
            cond_expr: 'Expression',
            post_expr: Optional['Expression'],
            stmts: StatementBlock
    ) -> None:
        super().__init__(cond_expr, stmts)
        self.init_expr = init_expr
        self.post_expr = post_expr

    def before_codes_callback(self, context: "Context", codes: List[str]) -> None:
        if self.init_expr is not None:
            codes += self.init_expr.to_tac(context)

    def before_jump_callback(self, context: "Context", codes: List[str]) -> None:
        if self.post_expr is not None:
            codes += self.post_expr.to_tac(context)

    def to_tac(self, context: "Context") -> List[str]:
        if self.init_expr is not None:
            self.init_expr.type_checker.check_type(context)
        if self.post_expr is not None:
            self.post_expr.type_checker.check_type(context)

        return super(ForStatement, self).to_tac(context)
