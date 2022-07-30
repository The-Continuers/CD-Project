from compiler.scanner import LexicalAnalyzer
from compiler.parser.run_one_test_case import run_test_case
from os import curdir

from compiler.type_checker import type_check
from compiler.utils import compose_list


def parent_path(dir: str) -> str:
    jj = '/'.join(dir.split('/')[:-1])
    if jj:
        jj += '/'
    return jj


def run(input_file_address: str) -> bool:
    with open(input_file_address) as input_file:
        data = input_file.read()
        parser = lambda: run_test_case(data, parent_path(input_file_address), raise_exception=True)
        res = compose_list(type_check, parser)()
        return True

    # analyzer = LexicalAnalyzer(data)
    # analyzer.analyze()
    # return analyzer.get_all_tokens()


if __name__ == '__main__':
    print(run('tests/test.d'))
