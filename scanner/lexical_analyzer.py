from functools import cached_property

from scanner.enums import *


class LexicalAnalyzer:

    def __init__(self, data: str):
        self.data = data

    @cached_property
    def preprocessor(self):
        from scanner import Preprocessor
        return Preprocessor(self)

    @cached_property
    def tokenizer(self):
        from scanner import Tokenizer
        return Tokenizer(self)

    def analyze(self):
        self.preprocessor.preprocess()
        self.tokenizer.tokenize()

    def clean_token_type(self, token) -> str:
        if token.type in ['RESERVED', 'PUNCTUATION']:
            return token.value
        elif token.type == 'UNDEFINED_TOKEN':
            return token.type
        else:
            return f"T_{token.type} {token.value}"

    def get_all_tokens(self) -> str:
        result = []
        while token := self.tokenizer.generate_token():
            result.append(self.clean_token_type(token))
        return "\n".join(result)
