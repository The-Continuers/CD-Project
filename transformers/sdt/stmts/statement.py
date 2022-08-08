from typing import List

from transformers.sdt import SDTNode


class Statement(SDTNode):
    pass


class StatementBlock(Statement):
    def __init__(self, sts: List[Statement]) -> None:
        super().__init__()
        self.sts = sts

    def to_tac(self, context: "Context") -> List[str]:
        codes = ["# Statements block start"]
        for st in self.sts:
            codes += st.to_tac(context=context)
        codes += ["# Statements block end"]
        return codes
