from typing import TYPE_CHECKING

from transformers.sdt import SDTNode
from transformers.sdt.utils import VariableName
from transformers.types import DecafType

if TYPE_CHECKING:
    from code_generation import Context


class Variable(SDTNode):

    def __init__(self, v_type: DecafType, v_id: VariableName) -> None:
        super().__init__()
        self.type = v_type
        self.id = v_id

    def to_tac(self, context: "Context"):
        x = self.id.name
        context.current_scope.extend_symbol(variable=self)
        return [f"# variable declaration for {self}",
                f"subu $sp, $sp, {self.type.size}	# Decrement sp to make space for variable {self}."]

    def __str__(self) -> str:
        return f"{self.type}: {self.id.name}"
