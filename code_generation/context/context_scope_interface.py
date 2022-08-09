from typing import TYPE_CHECKING

from code_generation import Scope

if TYPE_CHECKING:
    from code_generation.context import Context


class ContextScopeInterface:

    def __init__(self, context: "Context", scope_name: str):
        self.context = context
        self.scope_name = scope_name

    def __enter__(self):
        self.context.current_scope = Scope(
            name=self.scope_name, parent_scope=self.context.current_scope)
        return self.context.current_scope

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.current_scope = self.context.current_scope.parent_scope
