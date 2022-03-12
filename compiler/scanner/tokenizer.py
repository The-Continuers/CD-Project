import ply.lex as lex

from compiler.scanner import LexicalAnalyzer
from compiler.scanner.enums import *

# List of token names.This is always required
tokens = [] + DECAF_RESERVED_KEYWORDS

t_PUNCTUATION = r''  # TODO: Find them

t_ignore = ''  # TODO: Find them


def t_error(t):
    # TODO: Write this
    pass


class Tokenizer:
    def __init__(self, analyzer: LexicalAnalyzer):
        self.analyzer = analyzer
        self.lexer = lex.lex()

    def tokenize(self):
        self.lexer.input(self.analyzer.data)

    def generate_token(self):
        return self.lexer.token()
