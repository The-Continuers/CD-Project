from compiler.scanner import LexicalAnalyzer


class Preprocessor:

    def __init__(self, analyzer: LexicalAnalyzer):
        self.analyzer = analyzer

    def _preprocess(self) -> str:
        data = self.analyzer.data
        clean_data = ""
        micros = {}
        for line in data.splitlines():
            line = line.strip()
            arr = line.split(" ", 2)
            if "define" in arr:
                micros[arr[1]] = arr[2]
            else:
                clean_data += line
        self.analyzer.data = clean_data
        self.replace_micros(micros)
        return self.analyzer.data

    def replace_micros(self, micros):
        ...

    def preprocess(self):
        self.analyzer.data = self._preprocess()
