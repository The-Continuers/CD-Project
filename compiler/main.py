from compiler.scanner import LexicalAnalyzer
from compiler.parser.run_one_test_case import run_test_case


def run(input_file_address: str) -> bool:
    with open(input_file_address) as input_file:
        data = input_file.read()
        return True if run_test_case(data) == "OK" else False

    # analyzer = LexicalAnalyzer(data)
    # analyzer.analyze()
    # return analyzer.get_all_tokens()


if __name__ == '__main__':
    print(run('test.txt'))
