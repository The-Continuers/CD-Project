import operator
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from transformers.types import (
    DecafType, DecafBool, DecafInt, DecafArray
)
from transformers.types.exceptions import DecafTypeError

if TYPE_CHECKING:
    from code_generation import Context
    from transformers.sdt.stmts.expressions import (
        Expression,
        BinaryExpression,
        UnaryExpression,
        AssignExpression,
        CallExpression,
        IntValue,
        BoolValue,
        DoubleValue,
        StringValue,
        NullValue, DecafValue, RefExpression, InputExpression,
        ListExpression, IndexExpression
    )
    from transformers.sdt import Variable, Function

"""
from Bridge design.
see more on https://refactoring.guru/design-patterns/visitor
"""


class TypeChecker(ABC):

    def __init__(self, expression: "Expression"):
        self.expression: "Expression" = expression

    def __new__(cls, expression, *args, **kwargs):
        from transformers.sdt.stmts.expressions import (
            BinaryExpression,
            UnaryExpression,
            AssignExpression,
            CallExpression,
            IntValue,
            BoolValue,
            DoubleValue,
            StringValue,
            NullValue,
            ReadLine,
            ReadInteger,
            RefExpression,
            ListExpression,
            IndexExpression
        )
        return super().__new__(
            {
                BinaryExpression: BinaryExpressionTypeChecker,
                UnaryExpression: UnaryExpressionTypeChecker,
                AssignExpression: AssignExpressionTypeChecker,
                CallExpression: CallExpressionTypeChecker,
                RefExpression: RefExpressionTypeChecker,
                IntValue: ConstExpressionTypeChecker,
                BoolValue: ConstExpressionTypeChecker,
                DoubleValue: ConstExpressionTypeChecker,
                StringValue: ConstExpressionTypeChecker,
                NullValue: ConstExpressionTypeChecker,
                ReadLine: InputExpressionTypeChecker,
                ReadInteger: InputExpressionTypeChecker,
                ListExpression: ListExpressionTypeChecker,
                IndexExpression: IndexExpressionTypeChecker
            }[type(expression)],
        )

    def check_type_equality_and_return(self, t1: DecafType, t2: Optional[DecafType]):
        if t2 is not None:
            if t1 != t2:
                raise DecafTypeError(f'{t1} != {t2}')
        return t1

    @abstractmethod
    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        """
        checks whether an expression has a valid typing.

        Args:
            context: of type "compiler.code_generation.Context". It is mainly used for this expression.
            expected_type: the expected type (can be none if nothing is expected)
        Returns: the valid type of the expression
        Raises: "compiler.transformers.types.exceptions.DecafTypeError" on wrong typing.
        """
        pass


class BinaryExpressionTypeChecker(TypeChecker):
    expression: "BinaryExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        l_type, r_type = (
            self.expression.left.type_checker.check_type(context),
            self.expression.right.type_checker.check_type(context),
        )
        if l_type != r_type:
            raise DecafTypeError(f'{l_type} != {r_type}')
        if self.expression.op in [
            operator.gt, operator.ge, operator.lt, operator.le,
            operator.eq, operator.ne,
            operator.and_, operator.or_,
        ]:
            return self.check_type_equality_and_return(DecafBool, expected_type)
        return self.check_type_equality_and_return(l_type, expected_type)


class UnaryExpressionTypeChecker(TypeChecker):
    expression: "UnaryExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        if self.expression.op == operator.not_:
            return self.check_type_equality_and_return(DecafBool, expected_type)
        return self.expression.operand.type_checker.check_type(context, expected_type)


class AssignExpressionTypeChecker(TypeChecker):
    expression: "AssignExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        l_value_type = context.current_scope.apply_symbol(self.expression.l_value).type
        self.expression.r_value.type_checker.check_type(context, expected_type=l_value_type)
        return self.check_type_equality_and_return(t1=l_value_type, t2=expected_type)


class ConstExpressionTypeChecker(TypeChecker):
    expression: "DecafValue"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        return self.check_type_equality_and_return(self.expression.type, expected_type)


class CallExpressionTypeChecker(TypeChecker):
    expression: "CallExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        function: "Function" = context.current_scope.apply_function(
            self.expression.func_name)

        # check number of args
        if len(self.expression.args) != len(function.params):
            raise DecafTypeError(f'{function.identifier.name}_call: invalid number of arguments')

        # check type of args
        func_args = self.expression.args
        for i in range(len(func_args)):
            func_args[i].type_checker.check_type(context=context, expected_type=function.params[i].type)

        return self.check_type_equality_and_return(function.return_type, expected_type)


class RefExpressionTypeChecker(TypeChecker):
    expression: "RefExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        variable: "Variable" = context.current_scope.apply_symbol(
            self.expression.variable_name)
        return self.check_type_equality_and_return(variable.type, expected_type)


class InputExpressionTypeChecker(TypeChecker):
    expression: "InputExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        return self.check_type_equality_and_return(self.expression.return_type, expected_type)


class ListExpressionTypeChecker(TypeChecker):
    expression: "ListExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        self.expression.num_expr.type_checker.check_type(context=context, expected_type=DecafInt)
        return self.check_type_equality_and_return(t1=DecafArray(self.expression.type), t2=expected_type)


class IndexExpressionTypeChecker(TypeChecker):
    expression: "IndexExpression"

    def check_type(self, context: "Context", expected_type: DecafType = None) -> DecafType:
        array_t: "DecafType" = self.expression.array.type_checker.check_type(context=context)
        # check if l_value is of Array Type
        if not isinstance(array_t, DecafArray):
            raise DecafTypeError("IndexExpression: l_value is not of DecafArray")

        # check if index is of Int Type
        self.expression.index.type_checker.check_type(context=context, expected_type=DecafInt)
        return self.check_type_equality_and_return(t1=array_t.sub_type, t2=expected_type)
