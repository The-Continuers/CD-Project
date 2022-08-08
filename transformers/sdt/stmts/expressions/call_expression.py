from typing import List, TYPE_CHECKING

from code_generation import Scope, Context
from transformers.sdt.stmts.expressions import Expression, AssignExpression
from transformers.sdt.utils import VariableName

from transformers.sdt import Variable

if TYPE_CHECKING:
    from transformers.sdt import Function


class CallExpression(Expression):

    def __init__(self, func_name: VariableName, args: List[Expression]):
        self.func_name, self.args = func_name, args

    def to_tac(self, context: "Context"):
        func: "Function" = context.current_scope.apply_function(
            function_name=self.func_name)
        code = []
        # create params scope
        with context.scope(scope_name=f"{self.func_name.name}_scope"):
            # assign expression values to parameters
            for param_i in range(len(self.args)):
                func_param = func.params[param_i]
                # declare parameter variable
                param = Variable(v_id=VariableName(f"{self.func_name.name}_{func_param.id.name}"),
                                 v_type=func_param.type)
                code += param.to_tac(context)
                # compile assign expression code
                code += AssignExpression(l_value=param.id, r_value=self.args[param_i]) \
                    .to_tac(context=context)
            # jump to the label
            code += [f"jal {func.label}"]
            # pop params from the stack
            if len(func.params) != 0:
                func_params_fp = context.current_scope.apply_symbol_stack_pointer_offset(
                    variable_name=VariableName(
                        f"{self.func_name.name}_{func.params[0].id.name}")
                ) + func.params[0].type.size
                code += [
                    f"addiu $sp, $sp, {func_params_fp}\t# pop func params from the stack"
                ]
        return code
