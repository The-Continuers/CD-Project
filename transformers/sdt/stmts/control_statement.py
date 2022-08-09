from typing import TYPE_CHECKING, List

from transformers.sdt.stmts import Statement

if TYPE_CHECKING:
    from code_generation import Context


class ControlStatement(Statement):
    def __init__(self, loop_num: int) -> None:
        super().__init__()
        self.loop_num = loop_num


class BreakStatement(ControlStatement):

    def to_tac(self, context: "Context") -> List[str]:
        return [
            f'j {context.loop_stack.head().end_label}'
        ]


class ContinueStatement(ControlStatement):

    def to_tac(self, context: "Context") -> List[str]:
        return [
            f'j {context.loop_stack.head().continue_label}'
        ]
