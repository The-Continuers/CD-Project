from transformers.sdt import SDTNode
from transformers.types import TypeChecker


class Expression(SDTNode):

    @property
    def type_checker(self) -> TypeChecker:
        return TypeChecker(self)
