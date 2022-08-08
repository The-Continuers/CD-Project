from typing import List, Tuple

from os import listdir
from os.path import isfile, join

from lark import LarkError

from parser.parser import decaf_parser


def _get_inputs(dir_: str, current_files: List[str]):
    sub_folders = []
    for content in listdir(dir_):
        abs_path = join(dir_, content)
        if isfile(abs_path):
            if content.endswith('.d'):
                current_files.append(abs_path)
        else:
            sub_folders.append(abs_path)
    for sub_folder in sub_folders:
        _get_inputs(sub_folder, current_files)


def get_inputs(dir_: str) -> List[str]:
    inputs = []
    _get_inputs(dir_, inputs)
    return inputs


def run_test_case(code):
    tree = decaf_parser.parse(code)

def main():
    test_folder = 'tests'
    inputs = get_inputs(test_folder)
    bugs = []
    for input in inputs:
        try:
            with open(input, mode='r') as f:
                run_test_case(f.read())
        except LarkError:
            bugs.append(input)
    print(f'there are {len(bugs)} bugs')
    print(bugs)


if __name__ == '__main__':
    main()
