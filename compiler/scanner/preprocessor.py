from compiler.scanner import LexicalAnalyzer
import re

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
        data = self.analyzer.data
        for key, value in micros.items():
            data = re.sub(f'([^A-Za-z0-9_]){key}([^A-Za-z0-9_])', f'\\1{value}\\2', data)
        self.analyzer.data = data

    def preprocess(self):
        self.analyzer.data = self._preprocess()
