from typing import List, TYPE_CHECKING

from transformers.sdt import SDTNode
from transformers.types import DecafType, DecafInt
from transformers.sdt import Variable
from transformers.sdt.utils import VariableName

if TYPE_CHECKING:
    from code_generation import Scope
    from transformers.sdt.stmts import StatementBlock


class Function(SDTNode):

    @property
    def label(self) -> str:
        return f"func_{self.identifier.name}" if self.identifier.name != 'main' else 'main'

    def __init__(self, identifier: "VariableName", params: List["Variable"], return_type: DecafType,
                 stmts: "StatementBlock"):
        super().__init__()
        self.identifier, self.params, self.return_type = identifier, params, return_type
        self.stmts = stmts
        self.stmts.new_scope = False

    def to_tac(self, context: "Context"):
        scope_name = self.label
        context.current_scope.extend_function(self)
        with context.scope(scope_name=scope_name) as curr_scope:
            # push params to scope
            for param in self.params:
                curr_scope.extend_symbol(param)
            # push $fp, $ra to scope
            curr_scope.extend_symbol(variable=Variable(
                v_id=VariableName("$fp"), v_type=DecafInt))
            curr_scope.extend_symbol(variable=Variable(
                v_id=VariableName("$ra"), v_type=DecafInt))

            # saving and changing $fp, $ra code
            code = [
                "# saving and changing $fp, $ra code",
                "subu $sp, $sp, 8\t# decrement sp to make space to save ra, fp",
                "sw $fp, 4($sp)\t# save fp",
                "sw $ra, 0($sp)\t# save ra",
                "addiu $fp, $sp, 8\t# set up new fp",
            ]
            # init statements block
            code += self.stmts.to_tac(context=context)
            # TODO: return section should be in the Return statement
            # removing $fp and $ra from stack, and returning back to the prev. function
            code += [
                f"end_function_{self.label}:",
                "# removing $fp and $ra from stack, and returning back to the prev. function",
                "move $sp, $fp\t\t# pop callee frame off stack",
                "lw $ra, -8($fp)\t# restore saved ra",
                "lw $fp, -4($fp)\t# restore saved fp",
            ]
            # return section
            code += [
                f"jr $ra\t\t# return from function {self.label}"
            ]
        # indent and put label
        code = [f"{self.label}:"] + list(map(lambda x: f"\t{x}", code))
        return code
