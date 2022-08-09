from typing import TYPE_CHECKING, Callable, Any, List

from transformers.sdt.stmts.expressions import Expression
from transformers.types import DecafInt, DecafString, DecafBool, DecafDouble, DecafType, DecafNone, TypeChecker
from todos import Todo

if TYPE_CHECKING:
    from code_generation import Context


class DecafValue(Expression):
    caster: Callable[[str, ], Any]
    type: DecafType

    def get_caster(self):
        if self.caster is None:
            raise NotImplementedError
        return self.caster

    def __init__(self, value):
        self.value = self.get_caster()(value)

    def __str__(self) -> str:
        return f"{self.type}: {self.value}"

    def to_tac(self, context: "Context") -> List[str]:
        return ["# const expression evaluation"]


class IntValue(DecafValue):
    caster = int
    type = DecafInt

    def to_tac(self, context: "Context"):
        return super().to_tac(context) + \
            [f"li $t0, {self.value}\t# int value -> $t0"]


class StringValue(DecafValue):
    caster = str
    type = DecafString

    def to_tac(self, context: "Context"):
        context.add_data(
            data_name := context.get_data_name(data_type=DecafString),
            'asciiz',
            self.value
        )
        return super().to_tac(context) + \
            [
            f"la $t0, {data_name}\t# {data_name}'s address -> $t0"
        ]


class BoolValue(DecafValue):
    @staticmethod
    def caster(value):
        return {'false': False, 'true': True}[value]

    type = DecafBool

    def to_tac(self, context: "Context"):
        return super().to_tac(context) + \
            [
            f"li $t0, {int(self.value)}\t# bool value -> $t0",
        ]


class NullValue(DecafValue):
    @staticmethod
    def caster(_):
        return None

    type = DecafNone

    def to_tac(self, context: "Context"):
        return super().to_tac(context) + [str(Todo())]


class DoubleValue(DecafValue):
    caster = float
    type = DecafDouble

    def to_tac(self, context: "Context"):
        return super().to_tac(context) + \
            [
            f"li.d $f0, {self.value} \t# double value -> $f0"
        ]
