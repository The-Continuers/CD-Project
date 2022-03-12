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
        # print('preprocessed_data')
        # print(self.data)
        # print('preprocessed_data')
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
