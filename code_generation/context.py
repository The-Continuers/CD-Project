from code_generation import GLOBAL_SCOPE, Scope


class ContextScopeHandler:

    def __init__(self, context: "Context", scope_name: str):
        self.context = context
        self.scope_name = scope_name

    def __enter__(self):
        self.context.current_scope = Scope(
            name=self.scope_name, parent_scope=self.context.current_scope)
        return self.context.current_scope

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.current_scope = self.context.current_scope.parent_scope


def get_counter(modular: bool = False):
    def counter_generator():
        counter = 0
        while True:
            counter = counter + 1
            if modular:
                counter %= 2
            yield counter

    it_ = counter_generator()

    def counter():
        return it_.__next__()

    return counter


class Context:

    def __init__(self, current_scope: Scope = GLOBAL_SCOPE):
        self.current_scope: Scope = current_scope
        self.data_seg = []

        from transformers.types import (
            DecafInt, DecafDouble, DecafString, DecafBool
        )
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
        return ContextScopeHandler(self, scope_name=scope_name)

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
