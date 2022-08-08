from typing import List, TYPE_CHECKING

from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafInt, DecafString

if TYPE_CHECKING:
    from code_generation import Context
    from transformers.types import DecafType


class InputExpression(Expression):
    return_type: "DecafType"


class ReadInteger(InputExpression):
    return_type = DecafInt

    def to_tac(self, context: "Context") -> List[str]:
        return ["# ReadInteger expression",
                "# the result will be moved into $t0 in the function",
                "jal _ReadInteger"]


class ReadLine(InputExpression):
    return_type = DecafString

    def to_tac(self, context: "Context") -> List[str]:
        return ["# ReadInteger expression",
                "# the result will be moved into $t0 in the function",
                "jal _ReadLine"]
