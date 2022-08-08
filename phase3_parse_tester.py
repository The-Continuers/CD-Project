from typing import List, Tuple

from os import listdir
from os.path import isfile, join

from tqdm import tqdm

from parser.run_one_test_case import run_test_case


def get_subs(_dir: str, is_file: bool = False):
    return [f for f in listdir(_dir) if is_file == isfile(join(_dir, f))]


def get_inputs(_dir: str) -> List[str]:
    in_folders = get_subs(_dir)
    in_files = []
    for f in in_folders:
        in_files.extend([join(f, f1) for f1 in get_subs(
            _dir=join(_dir, f), is_file=True) if f1.endswith('.d')])
    return in_files


if __name__ == '__main__':
    test_folder = 'tests'
    bugs = []
    in_files = get_inputs(test_folder)
    for i in tqdm(range(len(in_files))):
        in_file = open(f"{test_folder}/{in_files[i]}")
        try:
            run_test_case(in_file.read(),
                          f'{test_folder}/', raise_exception=True)
        except Exception as e:
            bugs.append(in_files[i])
    print(bugs)
