import ply.lex as lex

from compiler.scanner import LexicalAnalyzer
from compiler.scanner.enums import *

# List of token names.This is always required
tokens = [
    'PUNCTUATION',
    'ID',
    'RESERVED',
    'BOOLEANLITERAL',
    'DOUBLELITERAL',
    'INTLITERAL',
    'STRINGLITERAL'
]


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# todo overlook
t_PUNCTUATION = r"(<=)|(>=)|(==)|(!=)|" \
                r"(&&)|(\|\|)|" \
                r"(\+=)|(-=)|(\*=)|(\/=)|" \
                r"[\.{}\[\],;()=\-!+*\/<>%]"


def t_ID(t):
    r"[_a-zA-Z][_a-zA-Z0-9]*"
    if t.value in DECAF_RESERVED_KEYWORDS:
        t.type = 'RESERVED'
    elif t.value in DECAF_BOOLEAN_KEYWORDS:
        t.type = 'BOOLEANLITERAL'
    return t


def t_DOUBLELITERAL(t):
    r"""[0-9]+\.[0-9]*([eE][-+]?[0-9]+)?"""
    # t.value = float(t.value)
    return t


def t_INTLITERAL(t):
    r"""(0x[0-9A-Fa-f]+)|([0-9]+)"""
    # t.value = int(t.value)
    return t


t_STRINGLITERAL = r"""\"([^\"\\]|(\\.))*\""""


def t_COMMENT(t):
    r"""(\/\/.*)|(\/\*([^\*]|(\*+[^\/\*]))*\*+\/)"""
    pass


t_ignore = " \t\f\v"


def t_error(t):
    t.type = 'UNDEFINED_TOKEN'
    t.lexer.lexpos = t.lexer.lexlen
    return t


class Tokenizer:
    def __init__(self, analyzer: LexicalAnalyzer):
        self.analyzer = analyzer
        self.lexer = lex.lex()

    def tokenize(self):
        self.lexer.input(self.analyzer.data)

    def generate_token(self):
        return self.lexer.token()
