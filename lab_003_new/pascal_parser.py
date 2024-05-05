import re

from graphviz import Digraph
from result import Ok, Err, Result, is_ok, is_err
from more_itertools import peekable

from pascal_lexer import PascalLexer, read_grammar, Token
from parse_error import ParseError


class ASTNode:
    def __init__(self, data) -> None:
        self.data = data
        self.children = []

    def print(self, tree = None, parent="", id = "main"):
        if not tree:
            tree = Digraph()
            tree.node_attr["shape"] = "plain"
        tree.node(id, str(self.data))
        if parent:
            tree.edge(parent, id)
        for i, child in enumerate(self.children):
            child.print(tree, id, id + "." + str(i))
        return tree

class PascalParser:
    def __init__(self, patterns) -> None:
        self.patterns = patterns

    def parse_var(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos[0]]
        match token:
            case Token(name="ID"):
                pos[0] += 1
                return Ok(ASTNode(token))
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
            return Ok(ASTNode(Token(name="INTEGER", value=parsed_int)))
        else:
            return Err("Unexpected integer pattern")

    def parse_rel_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("relOp")
        token = input[pos[0]]
        match token:
            case Token(name="RELOP"):
                pos[0] += 1
                root.children.append(ASTNode(token))
                return Ok(root)
            case _:
                return Err("Unexpected var pattern")

    def parse_plus_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("plusOp")
        token = input[pos[0]]
        match token:
            case Token(name="PLUSOP"):
                pos[0] += 1
                root.children.append(ASTNode(token))
                return Ok(root)
            case _:
                return Err("Unexpected var pattern")

    def parse_mult_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("multOp")
        token = input[pos[0]]
        match token:
            case Token(name="MULTOP"):
                pos[0] += 1
                root.children.append(ASTNode(token))
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
                return Ok(ASTNode(token))
            case _:
                return Err("Unexpected left paren")

    def parse_right_paren(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos[0]]
        match token:
            case Token(name="RIGHT_PAREN"):
                pos[0] += 1
                return Ok(ASTNode(token))
            case _:
                return Err("Unexpected right paren")

    def parse_factor(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("factor")
        mb_node = self.anyof([
            self.parse_const,
            self.parse_var,
            self.parse_integer,
            self.a([
                self.parse_left_paren,
                self.parse_arith_expr,
                self.parse_right_paren,
            ]),
        ])(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err
        return Ok(root)

    def parse_term(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("term")
        mb_node = self.anyof([
            self.parse_factor,
            self.a([
                self.parse_term,
                self.parse_mult_op,
                self.parse_factor,
            ]),
        ])(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
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
                return Ok(root)

        mb_node = self.parse_arith_expr(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err
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
                return Ok(root)

        mb_node = self.parse_arith_expr(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err

        return Ok(root)

    def parse_operator(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("operator")
        mb_var_node = self.parse_var(input, pos)
        match mb_var_node:
            case Ok(var_node):
                root.children.append(var_node)
            case err:
                return err

        token = input[pos[0]]
        match token:
            case Token(name='RELOP', value='='):
                root.children.append(ASTNode(token))
                pos[0] += 1
            case _:
                return Err(f"Unexpected RELOP token in pos: {pos}")

        mb_expr_node = self.parse_expr(input, pos)
        match mb_expr_node:
            case Ok(expr_node):
                root.children.append(expr_node)
            case err:
                return err

        return Ok(root)

    def parse_sep(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos[0]]
        match token:
            case Token(name="SEP"):
                pos[0] += 1
                return Ok(ASTNode(token))
            case _:
                return Err("Unexpected separator")

    def parse_operator_list(self, input, pos) -> Result[ASTNode, str]:       
        root = ASTNode("operator_list")
        mb_node = self.a([
            self.parse_operator,
            self.parse_sep
        ])(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)
            case err:
                return err

        mb_node = self.parse_operator_list(input, pos)
        match mb_node:
            case Ok(node):
                root.children.append(node)

        return Ok(root)

    def parse_block(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("block")
        token = input[pos[0]]
        match token:
            case Token(name='BEGIN'):
                pos[0] += 1
                root.children.append(ASTNode(token))
            case _:
                return Err(f"Unexpected BEGIN in pos: {pos[0]}")

        match self.parse_operator_list(input, pos):
            case Ok(operator_list_node):
                root.children.append(operator_list_node)
            case err:
                return err

        token = input[pos[0]]
        match token:
            case Token(name='END'):
                pos[0] += 1
                root.children.append(ASTNode(token))
            case _:
                return Err(f"Unexpected END in pos: {pos[0]}")

        return Ok(root)

    def parse_program(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("program")
        match self.parse_block(input, pos):
            case Ok(block_node):
                root.children.append(block_node)
            case err:
                return err
        return Ok(root)

    def parse(self, text) -> Result[ASTNode, str]:
        input = list(PascalLexer(self.patterns).lex(text))
        pos = [0]
        root = None
        try:
            root = ASTNode("root")
            match self.parse_program(input, pos):
                case Ok(program_node):
                    root.children.append(program_node)
                case err:
                    return err
        except StopIteration:
            return Err("Unexpected end of file")
        return Ok(root)

    def anyof(self, rules):
        def inner(input, pos) -> Result[ASTNode, str]:
            for rule in rules:
                mb_node = rule(input, pos)
                match mb_node:
                    case Ok(node):
                        return Ok(node)
                    case _:
                        pass
            return Ok(None)
        return inner

    def a(self, rules):
        def inner(input, pos) -> Result[ASTNode, str]:
            root = ASTNode("<proxy>")
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
