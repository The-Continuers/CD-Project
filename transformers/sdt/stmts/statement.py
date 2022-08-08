from typing import List, TYPE_CHECKING

from transformers.sdt import SDTNode

if TYPE_CHECKING:
    from code_generation import Context


class Statement(SDTNode):
    pass


class StatementBlock(Statement):
    def __init__(self, sts: List[Statement], new_scope: bool = True) -> None:
        super().__init__()
        self.sts = sts
        self.new_scope = new_scope

    def sts_to_tac(self, context: "Context") -> List[str]:
        codes = []
        for st in self.sts:
            codes += st.to_tac(context=context)
        return codes

    def to_tac(self, context: "Context") -> List[str]:
        codes = ["# Statements block start"]
        if self.new_scope:
            with context.scope(scope_name="block") as current_scope:
                codes += self.sts_to_tac(context)
                # TODO: check how much this code affect the others
                codes += [f"addi $sp, $sp, {current_scope.stack_size} # pop Statements Block Stack"]
        else:
            codes += self.sts_to_tac(context)
        codes += ["# Statements block end"]
        return codes
