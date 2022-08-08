from typing import TYPE_CHECKING, List

from code_generation import Context
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
        if var_type in [DecafInt, DecafBool, DecafString]:
            return [f"lw $t0, {st_offset}($sp)	# load constant value from {st_offset}($sp) to $t0"]
        elif var_type == DecafDouble:
            return [f"l.d $f0, {st_offset}($sp)	# load constant value from {st_offset}($sp) to $f0"]
        else:
            return [str(Todo())]

    def to_tac(self, context: "Context") -> List[str]:
        code = []
        l_variable = context.current_scope.apply_symbol(
            variable_name=self.variable_name)
        code += [f"# Variable Reference for {l_variable}"]
        code += self.ref_code(
            var=l_variable,
            st_offset=context.current_scope.apply_symbol_stack_pointer_offset(
                variable_name=self.variable_name
            )
        )
        return code
