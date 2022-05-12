from compiler.parser.parser import decaf_parser
from compiler.scanner import Preprocessor


class MockAnalyzer:

    def __init__(self, data: str):
        self.data = data


def run_test_case(text, raise_exception=False):
    try:
        analyzer = MockAnalyzer(text)
        Preprocessor(analyzer).preprocess()
        tree = decaf_parser.parse(analyzer.data)
        if raise_exception:
            return tree
        return "OK"
    except Exception as e:
        if raise_exception:
            raise e
        return "Syntax Error"


def run_test_case_by_file_name(test_case_name):
    in_file = open(f"resources/{test_case_name}")
    print(run_test_case(in_file.read(), raise_exception=True))


if __name__ == '__main__':
    run_test_case_by_file_name('t254-import4.in')