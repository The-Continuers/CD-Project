from typing import List, TYPE_CHECKING

from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafInt, DecafBool, DecafDouble, DecafString
from todos import Todo

if TYPE_CHECKING:
    from transformers.sdt.utils import VariableName
    from code_generation import Context
    from transformers.sdt import Variable


class AssignExpression(Expression):

    def __init__(self, l_value: "VariableName", r_value: Expression) -> None:
        super().__init__()
        self.l_value, self.r_value = l_value, r_value

    @staticmethod
    def assign_code(var: "Variable", st_offset: int) -> List[str]:
        var_type = var.type
        if var_type in [DecafInt, DecafBool, DecafString]:
            return [f"sw $t0, {st_offset}($sp)	# save value from $t0 to {st_offset}($sp)"]
        elif var_type == DecafDouble:
            return [f"s.d $f0, {st_offset}($sp)	# save value from $f0 to {st_offset}($sp)"]
        else:
            return [str(Todo())]

    def to_tac(self, context: "Context") -> List[str]:
        code = self.r_value.to_tac(context=context)
        l_variable = context.current_scope.apply_symbol(
            variable_name=self.l_value)
        code += [f"# Value assignment for {l_variable}"]
        code += self.assign_code(
            var=l_variable,
            st_offset=context.current_scope.apply_symbol_stack_pointer_offset(
                variable_name=self.l_value)
        )
        return code
