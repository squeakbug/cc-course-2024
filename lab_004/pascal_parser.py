import re

from result import Ok, Err, Result, is_ok, is_err
from more_itertools import peekable

from pascal_lexer import PascalLexer, read_grammar, Token
from parse_error import ParseError
from pascal_ast import ASTNode

class PascalParser:
    def __init__(self, patterns) -> None:
        self.patterns = patterns

    def parse_var(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos[0]]
        match token:
            case Token(name="ID"):
                pos[0] += 1
                return Ok(ASTNode(token, token.value))
            case _:
                return Err("Unexpected var pattern")

    def intTryParse(self, value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    def parse_integer(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos[0]]
        parsed_int, success = self.intTryParse(token.value)
        if success:
            pos[0] += 1
            data = Token(name="INTEGER", value=parsed_int)
            value = parsed_int
            return Ok(ASTNode(data, value))
        else:
            return Err("Unexpected integer pattern")

    def parse_rel_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("relOp")
        token = input[pos[0]]
        match token:
            case Token(name="RELOP"):
                pos[0] += 1
                root.value = token.value
                root.children.append(ASTNode(token, token.value))
                return Ok(root)
            case _:
                return Err("Unexpected var pattern")

    def parse_plus_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("plusOp")
        token = input[pos[0]]
        match token:
            case Token(name="PLUSOP"):
                pos[0] += 1
                root.value = token.value
                root.children.append(ASTNode(token, token.value))
                return Ok(root)
            case _:
                return Err("Unexpected var pattern")

    def parse_mult_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("multOp")
        token = input[pos[0]]
        match token:
            case Token(name="MULTOP"):
                pos[0] += 1
                root.value = token.value
                root.children.append(ASTNode(token, token.value))
                return Ok(root)
            case _:
                return Err("Unexpected var pattern")

    def parse_const(self, input, pos) -> Result[ASTNode, str]:
        return self.parse_var(input, pos)

    def parse_left_paren(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos[0]]
        match token:
            case Token(name="LEFT_PAREN"):
                pos[0] += 1
                return Ok(ASTNode(token, token.value))
            case _:
                return Err("Unexpected left paren")

    def parse_right_paren(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos[0]]
        match token:
            case Token(name="RIGHT_PAREN"):
                pos[0] += 1
                return Ok(ASTNode(token, token.value))
            case _:
                return Err("Unexpected right paren")

    def parse_factor(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("factor")
        (choise, mb_node) = self.anyof([
            self.parse_const,
            self.parse_var,
            self.parse_integer,
            self.a([
                self.parse_left_paren,
                self.parse_arith_expr,
                self.parse_right_paren,
            ], ASTNode("<proxy>")),
        ])(input, pos)
        match mb_node:
            case Ok(node):
                match choise:
                    case 0 | 1 | 2:
                        root.value = node.value
                    case 3:
                        root.value = " ".join([node.value for node in node.children])
            case err:
                return err
        return Ok(root)

    def parse_term(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("term")
        (choise, mb_node) = self.anyof([
            self.parse_factor,
            self.a([
                self.parse_term,
                self.parse_mult_op,
                self.parse_factor,
            ], ASTNode("<proxy>")),
        ])(input, pos)
        match mb_node:
            case Ok(node):
                match choise:
                    case 0:
                        root.value = node.value
                    case 1:
                        multop_val = node.children[1].value
                        term_val = node.children[2].value
                        factor_val = node.children[0].value
                        root.value = f"{multop_val} {term_val} {factor_val}"
            case err:
                return err
        return Ok(root)

    def parse_arith_expr(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("arith_expr")
        mb_node = self.parse_term(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err

        mb_node = self.parse_plus_op(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                root.value = root.children[0].value
                return Ok(root)

        mb_node = self.parse_arith_expr(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err

        term = root.children[2].value
        arith2 = root.children[0].value
        plusop = root.children[1].value
        root.value = f"{plusop} {term} {arith2}"
        return Ok(root)

    def parse_expr(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("expr")
        mb_node = self.parse_arith_expr(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err

        mb_node = self.parse_rel_op(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                root.value = root.children[0].value
                return Ok(root)

        mb_node = self.parse_arith_expr(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err

        arith1 = root.children[0].value
        arith2 = root.children[1].value
        relop = root.children[1].value
        root.value = f"{relop} {arith1} {arith2}"
        return Ok(root)

    def parse(self, text) -> Result[ASTNode, str]:
        input = list(PascalLexer(self.patterns).lex(text))
        pos = [0]
        root = None
        try:
            root = ASTNode("root")
            match self.parse_expr(input, pos):
                case Ok(expr_node):
                    root.value = expr_node.value
                    root.children.append(expr_node)
                case err:
                    return err
        except StopIteration:
            return Err("Unexpected end of file")
        return Ok(root)

    def anyof(self, rules) -> tuple[int, Result[ASTNode, str]]:
        def inner(input, pos) -> Result[ASTNode, str]:
            for i, rule in enumerate(rules):
                mb_node = rule(input, pos)
                match mb_node:
                    case Ok(node):
                        return (i, Ok(node))
                    case _:
                        pass
            return (-1, Ok(None))
        return inner

    def a(self, rules, root):
        def inner(input, pos) -> Result[ASTNode, str]:
            for rule in rules:
                mb_node = rule(input, pos)
                match mb_node:
                    case Ok(node):
                        root.children.append(node)
                    case err:
                        return err
            return Ok(root)
        return inner

if __name__ == '__main__':
    example = ""
    with open("examples/example_004.pas", "r") as f:
        example = f.read()
    rules, patterns = read_grammar("grammars/pascal.g")
    parser = PascalParser(patterns)
    ast = None
    match parser.parse(example):
        case Err(err):
            print(err)
            exit(-1)
        case Ok(ast):
            ast = ast
    ditree = ast.print()
    print(ditree)
