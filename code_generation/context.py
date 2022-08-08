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


class Context:

    def __init__(self, current_scope: Scope = GLOBAL_SCOPE):
        self.current_scope: Scope = current_scope
        self.data_seg = []
        self.sp = 0

    def scope(self, scope_name: str):
        return ContextScopeHandler(self, scope_name=scope_name)

    def add_data(self, name, mips_type, value):
        self.data_seg.append(
            f'{name}: .{mips_type} {value}'
        )
