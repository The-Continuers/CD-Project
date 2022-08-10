from typing import Any


class DecafType:

    def __init__(self, enum: str, size: int = 4):
        self.enum = enum
        self.size = size

    def __str__(self):
        return self.enum


class DecafArray(DecafType):

    def __init__(self, sub_type: DecafType):
        super().__init__(enum='Array')
        self.sub_type = sub_type

    def __str__(self):
        return f'{super().__str__()}<{str(self.sub_type)}>'

    def __eq__(self, other):
        # breakpoint()
        other_type = type(other)
        if other_type == DecafArray:
            return self.sub_type == other.sub_type
        else:
            # breakpoint()
            return other == DecafInt


DecafInt = DecafType(enum='DecafInt')
DecafBool = DecafType(enum='DecafBool')
DecafVoid = DecafType(enum='DecafVoid')
DecafDouble = DecafType(enum='DecafDouble', size=8)
DecafString = DecafType(enum='DecafString')
DecafNone = DecafType(enum='DecafNone')

if __name__ == '__main__':
    print(DecafArray(DecafArray(DecafString)))
