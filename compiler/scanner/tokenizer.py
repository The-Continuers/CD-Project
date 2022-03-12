import ply.lex as lex

from compiler.scanner import LexicalAnalyzer
from compiler.scanner.enums import *

# List of token names.This is always required
tokens = DECAF_RESERVED_KEYWORDS + [
             'PUNCTUATION',
             'ID',
             'INTLITERAL',
             'DOUBLELITERAL',
             'STRINGLITERAL',
             'BOOLEANLITERAL'
         ]


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# todo overlook
t_PUNCTUATION = r"(<<)|(>>)|(<=)|(>=)|(==)|(!=)|(&&)|(\|\|)|[{}\[\],;()=\-!+*\/<>%]"

t_ID = r"[_a-zA-Z][_a-zA-Z0-9]*"


def t_INTLITERAL(t):
    r"""(0x)?[0-9]+"""
    t.value = int(t.value)
    return t


def t_DOUBLELITERAL(t):
    r"""[0-9]+\.[0-9]+"""
    t.value = float(t.value)
    return t


t_STRINGLITERAL = r"""\"([^"]|(\\(\")?))*\""""

t_BOOLEANLITERAL = r"(true)|(false)"

t_ignore_COMMENT = r"""(\/\/.*)|(\/\*([^\*]|(\*+[^\/\*]))*\*+\/)"""

t_ignore = " \t"


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
