from compiler.parser.parser import decaf_parser


def run_test_case(test_case_name):
    in_file = open(f"resources/{test_case_name}")
    tree = decaf_parser.parse(in_file.read()).pretty()
    print(tree)


if __name__ == '__main__':
    run_test_case('t205-define.in')
