from typing import List, TYPE_CHECKING
from transformers.sdt.stmts import Statement
from transformers.sdt.stmts.expressions import Expression

if TYPE_CHECKING:
    from code_generation import Context


class StatementBlock(Statement):
    def __init__(self, sts: List[Statement], new_scope: bool = True) -> None:
        super().__init__()
        self.sts = sts
        self.new_scope = new_scope

    def sts_to_tac(self, context: "Context") -> List[str]:
        codes = []
        for st in self.sts:
            if isinstance(st, Expression):
                st.type_checker.check_type(context=context)
            codes += st.to_tac(context=context)
        return codes

    def to_tac(self, context: "Context") -> List[str]:
        codes = ["# Statements block start"]
        if self.new_scope:
            with context.scope() as current_scope:
                codes += self.sts_to_tac(context)
                # TODO: check how much this code affect the others
                codes += [f"addi $sp, $sp, {current_scope.stack_size} # pop Statements Block Stack"]
        else:
            codes += self.sts_to_tac(context)
        codes += ["# Statements block end"]
        return codes
