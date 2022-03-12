from compiler.scanner import LexicalAnalyzer


def run(input_file_address: str) -> str:
    with open(input_file_address) as input_file:
        data = input_file.read()

    analyzer = LexicalAnalyzer(data)
    analyzer.analyze()
    return analyzer.get_all_tokens()


if __name__ == '__main__':
    print(run('test.txt'))
