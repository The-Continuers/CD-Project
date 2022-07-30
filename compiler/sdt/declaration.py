from typing import *

from compiler.sdt.statement import Statement
from compiler.sdt.types import VariableType, FunctionType
from compiler.sdt.utils import VariableName


class Declaration:
    pass


class VariableDeclaration(Declaration):
    def __init__(self, var_type: VariableType, var: VariableName, *, const) -> None:
        super().__init__()
        self.type = var_type
        self.id = var
        # const initiation


class FunctionDeclaration(Declaration):
    def __init__(self, func_type: FunctionType, func_id: VariableName, params: List[VariableDeclaration],
                 stmts: List[Statement]) -> None:
        super().__init__()
        self.type = func_type
        self.id = func_id
        self.params = params
        self.stmts = stmts


class FieldDeclaration:
    pass


class ClassDeclaration(Declaration):
    def __init__(self, class_id: VariableName, fields: List[FieldDeclaration],
                 *, extend_class_id: VariableName, implements: List[VariableName]) -> None:
        super().__init__()
        self.id = class_id
        self.fields = fields
        # todo


class InterfacePrototype:
    pass


class InterfaceDeclaration(Declaration):
    def __init__(self, interface_id: VariableName, prototypes: InterfacePrototype) -> None:
        super().__init__()
        self.id = interface_id
        self.prototypes = prototypes
