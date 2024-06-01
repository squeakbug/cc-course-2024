import argparse

from pascal_lexer import read_grammar
from pascal_parser import PascalParser, Err, Ok

def main():
    parser = argparse.ArgumentParser(
                    prog='Нисходящий рекурсивный парсер',
                    description='Парсер паскаль-грамматики',
                    epilog='help')
    parser.add_argument('filename')
    args = parser.parse_args()

    example = ""
    with open(f"{args.filename}", "r") as f:
        example = f.read()
    _, patterns = read_grammar("grammars/pascal.g")
    parser = PascalParser(patterns)
    ast = None
    match parser.parse(example):
        case Err(err):
            print(err)
            exit(-1)
        case Ok(ast):
            ast = ast
    print("#", ast.value)
    ditree = ast.print()
    print(ditree)

if __name__ == "__main__":
    main()