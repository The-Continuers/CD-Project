from compiler.sdt.utils import VariableName


class Expression:
    pass


class OperationExpression(Expression):
    def __init__(self, operator):
        super(OperationExpression, self).__init__()
        self.operator = operator


class BinaryOperation(OperationExpression):
    def __init__(self, operator, l_operand: Expression, r_operand: Expression):
        super().__init__(operator)
        self.l_operand = l_operand
        self.r_operand = r_operand


class UnaryOperation(OperationExpression):
    def __init__(self, operator, operand: Expression):
        super().__init__(operator)
        self.operand = operand


class Assignment(Expression):
    def __init__(self, l_value: Expression, r_value: Expression):
        super(Assignment, self).__init__()
        self.l_value = l_value
        self.r_value = r_value


class IndexExpression(Expression):
    def __init__(self, iterable: Expression, index: Expression):
        super(IndexExpression, self).__init__()
        self.iterable = iterable
        self.index = index


class AccessExpression(Expression):
    def __init__(self, obj: Expression, var_name: VariableName):
        super(AccessExpression, self).__init__()
        self.obj = obj
        self.var_name = var_name
