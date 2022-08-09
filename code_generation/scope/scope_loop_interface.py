import typing

if typing.TYPE_CHECKING:
    from code_generation import Context
    from transformers.sdt.stmts import ForStatement, WhileStatement


class ScopeLoopInterface:

    def __init__(self, context: "Context", loop: typing.Union["ForStatement", "WhileStatement"]):
        self.context = context
        self.loop = loop

    def __enter__(self):
        self.context.loop_stack.push(self.loop)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.loop_stack.pop()
