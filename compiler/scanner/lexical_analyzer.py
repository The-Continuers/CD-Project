from functools import cached_property

from compiler.scanner.enums import *


class LexicalAnalyzer:

    def __init__(self, data: str):
        self.data = data

    @cached_property
    def preprocessor(self):
        from compiler.scanner import Preprocessor
        return Preprocessor(self)

    @cached_property
    def tokenizer(self):
        from compiler.scanner import Tokenizer
        return Tokenizer(self)

    def analyze(self):
        self.preprocessor.preprocess()
        self.tokenizer.tokenize()

    def clean_token_type(self, token) -> str:
        # TODO: Fill this function
        pass

    def get_all_tokens(self) -> str:
        result = ''
        while token := self.tokenizer.generate_token():
            result += self.judgment_format_write(token) + "\n"
        return result
