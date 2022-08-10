from typing import List, TYPE_CHECKING, Union

from code_generation.exceptions import DecafNotFoundInLocalError
from transformers.sdt.stmts.expressions import Expression, IndexExpression
from transformers.types import DecafInt, DecafBool, DecafDouble, DecafString
from todos import Todo
from transformers.sdt.utils import VariableName

if TYPE_CHECKING:
    from code_generation import Context
    from transformers.sdt import Variable


class AssignExpression(Expression):

    def __init__(self, l_value: Union["VariableName", "IndexExpression"], r_value: Expression) -> None:
        super().__init__()
        self.l_value, self.r_value = l_value, r_value

    @staticmethod
    def assign_code_to_stack(var: "Variable", st_offset: int) -> List[str]:
        var_type = var.type
        if var_type == DecafDouble:
            return [f"s.d $f0, {st_offset}($sp)	# save value from $f0 to {st_offset}($sp)"]
        else:
            return [f"sw $t0, {st_offset}($sp)	# save value from $t0 to {st_offset}($sp)"]

    @staticmethod
    def assign_to_head_of_stack(var, head_offset):
        var_type = var.type
        if var_type == DecafDouble:
            return [f"s.d $f0, {-head_offset}($v1)	# save value from $f0 to {head_offset}(head_of_stack)"]
        else:
            return [f"sw $t0, {-head_offset}($v1)	# save value from $t0 to {head_offset}(head_of_stack)"]

    def to_tac(self, context: "Context") -> List[str]:
        # breakpoint()
        # eval right
        code = self.r_value.to_tac(context=context)
        if type(self.l_value) == VariableName:
            l_variable = context.current_scope.apply_symbol(
                variable_name=self.l_value)
            code += [f"# Value assignment for {l_variable}"]

            try:
                code += self.assign_code_to_stack(
                    var=l_variable,
                    st_offset=context.current_scope.apply_symbol_stack_pointer_offset(
                        variable_name=self.l_value)
                )
            except DecafNotFoundInLocalError:
                code += self.assign_to_head_of_stack(
                    var=l_variable,
                    head_offset=context.current_scope.global_address(variable_name=self.l_value)
                )
        elif type(self.l_value) == IndexExpression:
            # put eval right to stack
            r_type = self.r_value.type_checker.check_type(context=context)
            code += context.current_scope.push_to_stack(temp_t=r_type)
            # eval left
            code += self.l_value.to_tac(context=context)
            # because index is always 4bytes, we use $t0
            code += [f"move $t1, $t0 # move left evaluated index to $t1"]
            # pop right from stack
            code += context.current_scope.pop_from_stack(temp_t=r_type)
            if r_type == DecafDouble:
                code += [f"s.d $f0, 0($t1)	# save value from $f0 to 0($t1)"]
            else:
                code += [f"sw $t0, 0($t1)	# save value from $t0 to 0($t1)"]
        else:
            code += [str(Todo())]

        return code
