from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transformers.sdt import Variable


class Symbol:

    def __init__(self, variable: "Variable", relative_stack_address: int):
        self.variable = variable
        self.relative_stack_address = relative_stack_address

    def __str__(self):
        return str((str(self.variable), self.relative_stack_address))
