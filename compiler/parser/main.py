from typing import List, Tuple

from compiler.parser.parser import decaf_parser

from os import listdir
from os.path import isfile, join


def get_inputs(dir: str) -> Tuple[List[str], List[str]]:
    in_files = [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('.in')]
    out_files = [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('.out')]
    in_files.sort()
    out_files.sort()
    return in_files, out_files


def handle(text: str) -> str:
    try:
        tree = decaf_parser.parse(text)
        return "OK"
    except:
        return "SYNTAX ERROR"


if __name__ == '__main__':
    bugs = []
    in_files, out_files = get_inputs('resources')
    for i in range(len(in_files)):
        # assert '.'.join(in_files[i].split('.')[:-1]) == '.'.join(out_files[i].split('.')[:-1]), f"{in_files[i]}"
        in_file = open(f"resources/{in_files[i]}")
        out = handle(in_file.read())
        out_file = open(f"resources/{out_files[i]}")
        exp_out = out_file.read()
        if out.lower() != exp_out.lower():
            bugs.append(in_files[i])
    print(f"{len(bugs)} bugs")
    print('\n'.join(bugs))
