import json
import os
from abc import ABCMeta
from typing import Type, List

from lark import Transformer, Tree

from transformers.mixins import DecafExpressionTransformerMixin, DecafToValueTransformerMixin
from transformers.sdt import (
    SDTNode, Variable, Function,
)
from transformers.sdt.stmts import ReturnStatement, IfStatement, WhileStatement, ForStatement, BreakStatement, \
    ContinueStatement, PrintStatement, StatementBlock
from transformers.sdt.stmts.expressions import AssignExpression, AccessExpression, IndexExpression, \
    CallExpression, ListExpression, RefExpression, ReadLine, ReadInteger
from transformers.sdt.utils import VariableName
from transformers.types import (
    DecafArray, DecafString, DecafBool, DecafDouble, DecafInt, DecafVoid,
)
from todos import Todo


class DecafTransformerMeta(ABCMeta):

    @staticmethod
    def set_go_one_level_furthers(obj: Type["DecafTransformer"]):
        def go_one_level_further_func(self, tree):
            return tree[0]

        for go_one_level_further in obj.go_one_level_furthers:
            setattr(obj, go_one_level_further, go_one_level_further_func)

    @staticmethod
    def get_to_expr(expr_w_operator):
        def to_expr(self, tree):
            return expr_w_operator.expr_class(expr_w_operator.operator, *tree)

        return to_expr

    @classmethod
    def set_expressions(cls, obj: Type["DecafTransformer"]):
        for expr_label, expr_w_operator in obj.expr_label_to_expression.items():
            setattr(obj, expr_label, cls.get_to_expr(expr_w_operator))

    @staticmethod
    def get_to_value(caster):
        def to_value(self, tree):
            return caster(tree[0].value)

        return to_value

    @classmethod
    def set_to_values(cls, obj: Type["DecafTransformer"]):
        for label, caster in obj.to_value_derivations.items():
            setattr(obj, label, cls.get_to_value(caster))

    def __new__(cls, name, bases, classdict):
        cls_obj: Type[DecafTransformer] = type.__new__(
            cls, name, bases, dict(classdict))
        setters = [
            'set_go_one_level_furthers',
            'set_expressions',
            'set_to_values',
        ]
        for setter in setters:
            getattr(cls, setter)(cls_obj)
        return cls_obj


def scrape_safe(tree, index, return_value=None):
    try:
        return tree[index]
    except IndexError:
        return return_value


class DecafTransformer(
    DecafToValueTransformerMixin,
    DecafExpressionTransformerMixin,
    Transformer,
    metaclass=DecafTransformerMeta
):
    with open('transformers/resources/go_one_level_furthers.json') as f:
        go_one_level_furthers = json.loads(f.read())

    def __init__(self, visit_tokens: bool = True) -> None:
        super().__init__(visit_tokens)
        self.loop_nums = 0

    def program(self, tree: List[SDTNode]):
        # create global context object
        from code_generation import Context
        context = Context()

        # calc. code section
        code_section = [".globl main",
                        ".text"]
        for tr in tree:
            tr.check_scope()
            code_section += tr.to_tac(context)
        with open(os.path.join(os.path.dirname(__file__), '../code_generation/resources/funcs.reserved'), 'r') as f:
            code_section += f.read().split('\n')

        # calc. data section
        data_section = [".data"]
        data_section += context.data_seg
        with open(os.path.join(os.path.dirname(__file__), '../code_generation/resources/data.reserved'), 'r') as f:
            data_section += f.read().split('\n')

        code = data_section + code_section

        return '\n'.join(code)

    def variable_defined(self, tree):
        return Variable(v_type=tree[0], v_id=tree[1])

    def variable_defined_with_assign(self, tree):
        return StatementBlock(sts=[Variable(v_type=tree[0], v_id=tree[1]),
                                   AssignExpression(l_value=tree[1], r_value=tree[2])])

    # types
    def type_int(self, tree):
        return DecafInt

    def type_double(self, tree):
        return DecafDouble

    def type_bool(self, tree):
        return DecafBool

    def type_string(self, tree):
        return DecafString

    def type_identifier(self, tree):
        Todo()
        return tree[0]

    def type_array(self, tree):
        return DecafArray(tree[0])

    def typed_function_declared(self, tree):
        return Function(return_type=tree[0], identifier=tree[1], params=tree[2], stmts=tree[3])

    def void_function_declared(self, tree):
        return Function(return_type=DecafVoid, identifier=tree[0], params=tree[1], stmts=tree[2])

    def formals_variable(self, tree):
        return tree

    def formals_empty(self, tree):
        return list()

    def new_class(self, tree):
        pass

    def extends_identifier(self, tree):
        pass

    def extends_identifier_empty(self, tree):
        pass

    def implements_identifier(self, tree):
        pass

    def implements_identifier_empty(self, tree):
        pass

    def statement_block(self, tree):
        if len(tree) == 1 and isinstance(tree[0], StatementBlock):
            return tree[0]
        else:
            return StatementBlock(sts=tree)

    def return_statement(self, tree):
        return ReturnStatement(tree[0])

    def optional_expression_statement(self, tree):
        return scrape_safe(tree, 0)

    def if_statement(self, tree):
        return IfStatement(tree[0], tree[1], scrape_safe(tree, 2))

    def while_statement(self, tree):
        self.loop_nums += 1
        return WhileStatement(cond_expr=tree[0], stmts=tree[1])

    def for_statement(self, tree):
        self.loop_nums += 1
        return ForStatement(init_expr=tree[0], cond_expr=tree[1], post_expr=tree[2], stmts=tree[3])

    def break_statement(self, tree):
        return BreakStatement(loop_num=self.loop_nums)

    def continue_statement(self, tree):
        return ContinueStatement(loop_num=self.loop_nums)

    def print_statement(self, tree):
        return PrintStatement(exprs=tree)

    def assign(self, tree):
        return AssignExpression(tree[0], tree[1])

    def lv_call(self, tree):
        return CallExpression(tree[0], tree[1])

    def args(self, tree):
        return tree

    def empty_args(self, tree):
        return list()

    def expr_instantiate(self, tree):
        return Todo()

    def expr_instantiate_array(self, tree):
        return ListExpression(array_expr=tree[0], array_type=tree[1])

    def expr_dts(self, tree):
        return Todo()

    def expr_this(self, tree):
        return Todo()

    def read_integer(self, tree):
        return ReadInteger()

    def read_line(self, tree):
        return ReadLine()

    def lv_id(self, tree):
        return RefExpression(tree[0])
