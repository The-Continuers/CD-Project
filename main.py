import getopt
import sys
from os.path import join
from typing import List

from parser.run_one_test_case import run_test_case

from transformers.decaf_transformer import DecafTransformer


def parent_path(dir: str) -> str:
    jj = '/'.join(dir.split('/')[:-1])
    if jj:
        jj += '/'
    return jj


def run(input_file_address: str) -> bool:
    with open(input_file_address) as input_file:
        data = input_file.read()
        parse_tree = run_test_case(data, parent_path(
            input_file_address), raise_exception=True)
        tac_code = DecafTransformer().transform(parse_tree)
        return tac_code


def eval_test():
    file_folder = 'tests/'
    test_folder = 'ConditionalStatements/'
    file_name = 't139-cond-5.d'
    tac_code = run(join(file_folder, test_folder, file_name))

    output_file_addr = "out.asm"
    with open(output_file_addr, "w") as output_file:
        print(tac_code, file=output_file)


def get_sys_attrs(argv, short_attrs: List[str] = [], long_attrs: List[str] = []) -> List:
    short_attrs_string: str = ':'.join(short_attrs) + ':'
    long_attrs_list = list(map(lambda l_attr: f"{l_attr}=", long_attrs))
    try:
        opts, args = getopt.getopt(argv, f"h{short_attrs_string}", long_attrs_list)
    except getopt.GetoptError:
        print('main.py -a <inputfile> -b <inputfile> -o <outputfile>')
        sys.exit(2)

    # opts based on run.sh, should be sth like: [('-i', 'G1/1.d'), ('-o', 'G1/1.s')]
    return list(map(lambda attr: attr[1], opts))


def eval_global_test(argv):
    in_dir = 'tests'
    out_dir = 'out'
    input_file_local_addr, output_file_local_addr = get_sys_attrs(argv=argv, short_attrs=['i', 'o'])
    tac_code = run(join(in_dir, input_file_local_addr))

    output_file_addr = join(out_dir, output_file_local_addr)
    with open(output_file_addr, "w") as output_file:
        print(tac_code, file=output_file)


if __name__ == '__main__':
    eval_test()
    # eval_global_test(argv=sys.argv[1:])
