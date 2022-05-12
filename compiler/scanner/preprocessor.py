import random

from compiler.scanner import LexicalAnalyzer
import re

INSIDE_QUOTATION_REGEX_TEMPLATE = r'("[^"\\]*(?:\\.[^"\\]*)*")|\b{0}\b'
IMPORT_FILE_REGEX = r'^import\s+"(\S+)"$'
IMPORT_REGEX = r'^import\s+\S+$'


class Preprocessor:

    def __init__(self, analyzer: LexicalAnalyzer):
        self.analyzer = analyzer
        self.tof_key = f'ashk{random.randint(1000, 9999)}sep{random.randint(1000, 9999)}sad'
        self.import_pattern = re.compile(IMPORT_REGEX)
        self.import_file_pattern = re.compile(IMPORT_FILE_REGEX)

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
        new_data_parts = []
        macros = {}
        selected_line = False
        for line in data.splitlines():
            line = line.strip()
            import_file_match = self.import_file_pattern.match(line)
            import_line_match = self.import_pattern.match(line)
            arr = line.split(" ", 2)
            if arr[0] == "define":
                if selected_line:
                    raise Exception
                if len(arr) == 3:
                    macros[arr[1]] = arr[2]
                else:
                    raise Exception
            else:
                is_import_line = bool(import_file_match) or bool(import_line_match)
                if not bool(import_file_match):
                    if not is_import_line:
                        selected_line = True
                    new_data_parts.append(line)
                else:
                    new_data_parts.append(self.handle_import_file(import_file_match))
        return self.replace_micros('\n'.join(new_data_parts), macros)

    def handle_import_file(self, match):
        try:
            f = open(f'{self.analyzer.parent_path}{match.group(1)}')
            text = f.read()
        except:
            text = ""
        return text

    def preprocess(self):
        self.analyzer.data = self._preprocess()
