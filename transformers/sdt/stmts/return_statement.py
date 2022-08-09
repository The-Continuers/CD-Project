from typing import List, TYPE_CHECKING

from transformers.sdt.stmts import Statement
from transformers.sdt.stmts.expressions import Expression
from transformers.sdt.utils import VariableName

if TYPE_CHECKING:
    from code_generation import Context
    from transformers.types import DecafType


class ReturnStatement(Statement):
    def __init__(self, return_expr: Expression):
        self.return_expr = return_expr

    @staticmethod
    def get_func_name(context: "Context") -> str:
        return context.current_scope.get_name()

    def to_tac(self, context: "Context") -> List[str]:
        """
            if there exists a return value, it'll be stored in $t0 or $f0.
            therefore, after function return, the assign expression will use that $t0 or $f0,
            considering type-safety issues
        """
        self.type_check(context=context)
        codes = ["# return expression"]
        if self.return_expr is not None:
            codes += self.return_expr.to_tac(context=context)
        codes += [f'j end_function_{self.get_func_name(context=context)} # Fuck Life']
        return codes

    def type_check(self, context: "Context") -> "DecafType":
        func_label = self.get_func_name(context=context)
        # tof
        func_name = func_label if func_label == "main" else func_label[5:]
        # breakpoint()
        func_return_type: "DecafType" = context.current_scope.apply_function(
            function_name=VariableName(func_name)).return_type
        if self.return_expr is not None:
            return self.return_expr.type_checker.check_type(context=context,
                                                            expected_type=func_return_type)
