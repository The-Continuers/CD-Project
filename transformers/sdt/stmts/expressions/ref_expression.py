from typing import TYPE_CHECKING, List

from code_generation import Context
from code_generation.exceptions import DecafNotFoundInLocalError
from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafString, DecafInt, DecafBool, DecafDouble
from todos import Todo

if TYPE_CHECKING:
    from transformers.sdt.utils import VariableName
    from transformers.sdt import Variable


class RefExpression(Expression):

    def __init__(self, variable_name: "VariableName"):
        self.variable_name = variable_name

    @staticmethod
    def ref_code(var: "Variable", st_offset: int) -> List[str]:
        var_type = var.type
        if var_type == DecafDouble:
            return [f"l.d $f0, {st_offset}($sp)	# load constant value from {st_offset}($sp) to $f0"]
        else:
            return [f"lw $t0, {st_offset}($sp)	# load constant value from {st_offset}($sp) to $t0"]

    @staticmethod
    def ref_to_head_of_stack(var, head_offset):
        var_type = var.type
        if var_type == DecafDouble:
            return [f"l.d $f0, {-head_offset}($v1)	# save value from $f0 to {head_offset}(head_of_stack)"]
        else:
            return [f"lw $t0, {-head_offset}($v1)	# save value from $t0 to {head_offset}(head_of_stack)"]

    def to_tac(self, context: "Context") -> List[str]:
        code = []
        l_variable = context.current_scope.apply_symbol(
            variable_name=self.variable_name)
        code += [f"# Variable Reference for {l_variable}"]
        try:
            code += self.ref_code(
                var=l_variable,
                st_offset=context.current_scope.apply_symbol_stack_pointer_offset(
                    variable_name=self.variable_name
                )
            )
        except DecafNotFoundInLocalError:
            code += self.ref_to_head_of_stack(
                var=l_variable,
                head_offset=context.current_scope.global_address(variable_name=self.variable_name)
            )
        return code
