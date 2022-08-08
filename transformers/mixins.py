import operator
from collections import namedtuple
from typing import Dict, Callable

from transformers.sdt.stmts.expressions import IntValue, DoubleValue, BoolValue, NullValue, StringValue
from transformers.sdt.stmts.expressions import BinaryExpression, UnaryExpression
from transformers.sdt.utils import VariableName

ExpressionWithOperator = namedtuple(
    'ExpressionWithOperator', ['expr_class', 'operator'])


class DecafExpressionTransformerMixin:
    expr_label_to_expression: Dict[str, ExpressionWithOperator] = {
        'or': ExpressionWithOperator(BinaryExpression, operator.or_),
        'and': ExpressionWithOperator(BinaryExpression, operator.and_),
        'equals': ExpressionWithOperator(BinaryExpression, operator.eq),
        'n_equals': ExpressionWithOperator(BinaryExpression, operator.ne),
        'lt': ExpressionWithOperator(BinaryExpression, operator.lt),
        'lte': ExpressionWithOperator(BinaryExpression, operator.le),
        'gt': ExpressionWithOperator(BinaryExpression, operator.gt),
        'gte': ExpressionWithOperator(BinaryExpression, operator.ge),
        'add': ExpressionWithOperator(BinaryExpression, operator.add),
        'sub': ExpressionWithOperator(BinaryExpression, operator.sub),
        'mult': ExpressionWithOperator(BinaryExpression, operator.mul),
        'div': ExpressionWithOperator(BinaryExpression, operator.truediv),
        'mod': ExpressionWithOperator(BinaryExpression, operator.mod),
        'neg': ExpressionWithOperator(UnaryExpression, operator.neg),
        'not': ExpressionWithOperator(UnaryExpression, operator.not_),
    }


class DecafToValueTransformerMixin:
    to_value_derivations: Dict[str, Callable] = {
        'identifier': VariableName,
        'int_const': IntValue,
        'double_const': DoubleValue,
        'bool_const': BoolValue,
        'null_const': NullValue,
        'string_const': StringValue,
    }
