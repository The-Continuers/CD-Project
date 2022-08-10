from typing import Union, TYPE_CHECKING

from code_generation import GLOBAL_SCOPE, Scope
from code_generation.context import get_counter, ContextScopeInterface, ContextLoopInterface
from transformers.types import DecafType, DecafInt, DecafDouble, DecafString, DecafBool
from utils import Stack

if TYPE_CHECKING:
    from transformers.sdt.stmts import ForStatement, WhileStatement


class Context:

    def __init__(self, current_scope: Scope = GLOBAL_SCOPE):
        self.current_scope: Scope = current_scope
        self.data_seg = []
        self.loop_stack = Stack()
        self.decaf_type_to_counter = {
            DecafInt: get_counter(),
            DecafDouble: get_counter(),
            DecafString: get_counter(),
            DecafBool: get_counter(),
        }
        self.loop_counter = get_counter()
        self.if_else_counter = {
            'if': get_counter(),
            'else': get_counter(),
        }

    def scope(self, scope_name: str = None):
        return ContextScopeInterface(self, scope_name=scope_name)

    def loop(self, loop: Union["ForStatement", "WhileStatement"]):
        return ContextLoopInterface(self, loop)

    def add_data(self, name, mips_type, value):
        self.data_seg.append(
            f'{name}: .{mips_type} {value}'
        )

    def get_data_name(self, data_type: "DecafType") -> str:
        return f"{self.current_scope.scope_prefix}_{data_type.enum}_const_{self.decaf_type_to_counter[data_type]()}"

    def get_end_if_else_label(self, if_else) -> str:
        return f'end_{if_else}_{self.current_scope.scope_prefix}_{self.if_else_counter[if_else]()}'

    def get_loop_label(self) -> str:
        return f'loop_{self.current_scope.scope_prefix}_{self.loop_counter()}'
