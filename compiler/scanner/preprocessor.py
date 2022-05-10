import random

from compiler.scanner import LexicalAnalyzer
import re

INSIDE_QUOTATION_REGEX_TEMPLATE = r'("[^"\\]*(?:\\.[^"\\]*)*")|\b{0}\b'


class Preprocessor:

    def __init__(self, analyzer: LexicalAnalyzer):
        self.analyzer = analyzer
        self.tof_key = f'ashk{random.randint(1000, 9999)}sep{random.randint(1000, 9999)}sad'

    def replace_micros(self, data, macros):
        for key, value in macros.items():
            data = re.sub(
                INSIDE_QUOTATION_REGEX_TEMPLATE.format(key),
                lambda m: m.group(1) if m.group(1) else self.tof_key,
                data,
            )
            data = re.sub(fr'([^A-Za-z0-9_])?{self.tof_key}([^A-Za-z0-9_])?', f'\g<1>{value}\g<2>', data)
            data = re.sub(f'{self.tof_key}', f'{key}', data)
        return data

    def _preprocess(self) -> str:
        data = self.analyzer.data
        clean_data = ""
        macros = {}
        selected_line = False
        for line in data.splitlines():
            line = line.strip()
            arr = line.split(" ", 2)
            if arr[0] == "define":
                if selected_line:
                    raise Exception
                if len(arr) == 3:
                    macros[arr[1]] = arr[2]
                else:
                    raise Exception
            else:
                selected_line = True
                clean_data += line
                clean_data += '\n'
        return self.replace_micros(clean_data, macros)

    def preprocess(self):
        self.analyzer.data = self._preprocess()
