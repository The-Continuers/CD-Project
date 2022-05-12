from typing import List, Tuple

from os import listdir
from os.path import isfile, join

from compiler.parser.run_one_test_case import run_test_case


def get_inputs(dir: str) -> Tuple[List[str], List[str]]:
    in_files = [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('.in') and 'file' not in f]
    out_files = [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('.out')]
    in_files.sort()
    out_files.sort()
    return in_files, out_files


if __name__ == '__main__':
    bugs = []
    in_files, out_files = get_inputs('resources')
    for i in range(len(in_files)):
        in_file = open(f"resources/{in_files[i]}")
        out_file = open(f"resources/{out_files[i]}")
        exp_out = out_file.read()
        out = run_test_case(in_file.read(), 'resources/')
        if out.strip().lower() != exp_out.strip().lower():
            bugs.append(in_files[i])
    print(f"{len(bugs)} bugs")
    print('\n'.join(bugs))
