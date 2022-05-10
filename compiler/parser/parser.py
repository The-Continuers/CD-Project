from lark import Lark

from compiler.parser.grammars import G2

decaf_parser = Lark(
    grammar=G2,
    start="program",
    parser="lalr",
)
