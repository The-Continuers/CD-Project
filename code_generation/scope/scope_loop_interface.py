import typing


if typing.TYPE_CHECKING:
    from code_generation import Scope
    from transformers.sdt.stmts import ForStatement, WhileStatement


class ScopeLoopInterface:

    def __init__(self, scope: "Scope", loop: typing.Union["ForStatement", "WhileStatement"]):
        self.scope = scope
        self.loop = loop

    def __enter__(self):
        self.scope.loop_stack.push(self.loop)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scope.loop_stack.pop()
