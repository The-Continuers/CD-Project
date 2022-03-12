from compiler.scanner import LexicalAnalyzer


class Preprocessor:

    def __init__(self, analyzer: LexicalAnalyzer):
        self.analyzer = analyzer

    def _preprocess(self) -> str:
        # TODO: Sad
        return self.analyzer.data

    def preprocess(self):
        self.analyzer.data = self._preprocess()
