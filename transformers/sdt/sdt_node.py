from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from code_generation import Context


class SDTNode:
    def to_tac(self, context: "Context") -> List[str]:
        return []

    def check_scope(self):
        pass
