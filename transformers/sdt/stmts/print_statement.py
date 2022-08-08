from typing import TYPE_CHECKING, List

from transformers.sdt.stmts import Statement
from transformers.types import DecafInt, DecafDouble, DecafBool, DecafString, DecafType

if TYPE_CHECKING:
    from transformers.sdt.stmts.expressions import Expression
    from code_generation import Context


class PrintStatement(Statement):
    type_to_print_mips_code = {
        DecafInt: [f'jal _PrintInt'],
        DecafDouble: [f'jal _SimplePrintDouble'],
        DecafBool: [f'jal _PrintBool'],
        DecafString: [f'jal _PrintString'],
    }

    def __init__(self, exprs: List['Expression']) -> None:
        super().__init__()
        self.exprs = exprs

    def to_tac(self, context: "Context") -> List[str]:
        codes: List[str] = []
        for expr in self.exprs:
            codes += expr.to_tac(context)
            expr_ty: DecafType = expr.type_checker.check_type(context)
            codes += [
                "# push print expression to stack",
                *context.current_scope.push_to_stack(temp_t=expr_ty),
            ]
            codes += self.type_to_print_mips_code.get(expr_ty)
            codes += [
                "# pop print expression from stack",
                *context.current_scope.pop_from_stack(temp_t=expr_ty)
            ]
        codes += ['jal _PrintNewLine']
        return codes
