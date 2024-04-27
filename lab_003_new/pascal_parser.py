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
        token = input[pos]
        pos += 1
        match token:
            case Token(name="ID"):
                print(token)
                return Ok(ASTNode(token))
            case _:
                return Err("Unexpected var pattern")

    def intTryParse(value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    def parse_integer(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos]
        pos += 1
        parsed_int, success = self.intTryParse(token)
        if success:
            return Ok(ASTNode(parsed_int))
        else:
            return Err("Unexpected integer pattern")

    def parse_rel_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("relOp")

        token = input[pos]
        pos += 1
        if token in self.rel_ops:
            rel_op_node = ASTNode(token)
            root.children.append(rel_op_node)

        return root

    def parse_plus_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("plusOp")

        token = input[pos]
        pos += 1
        if token in self.plus_ops:
            plus_op_node = ASTNode(token)
            root.children.append(plus_op_node)

        return root

    def parse_mult_op(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("multOp")

        token = input[pos]
        pos += 1
        if token in self.mult_ops:
            mult_op_node = ASTNode(token)
            root.children.append(mult_op_node)

        return root

    def parse_const(self, input, pos) -> Result[ASTNode, str]:
        return self.parse_var(input, pos)

    def parse_left_paren(self, input, pos) -> Result[ASTNode, str]:
        token = input[pos]
        pos += 1
        if token == "(":
            return Ok(ASTNode(token))
        else:
            return Err("Unexpected left paren")

    def parse_right_paren(self, input, pos) -> Result[ASTNode, str]:
        token = input
        pos += 1
        if token == ")":
            return Ok(ASTNode(token))
        else:
            return Err("Unexpected right paren")

    def parse_factor(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("factor")
        node = self.anyof([
            self.parse_const,
            self.parse_var,
            self.a([
                self.parse_left_paren,
                self.parse_arith_expr,
                self.parse_right_paren,
            ]),
        ])(input, pos)
        root.children.append(node)
        return root

    def parse_term(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("term")
        node = self.anyof([
            self.parse_factor,
            self.a([
                self.parse_term,
                self.parse_mult_op,
                self.parse_factor,
            ]),
        ])(input, pos)
        root.children.append(node)
        return root

    def parse_arith_expr(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("arith_expr")
        node = self.anyof([
            self.parse_term,
            self.a([
                self.parse_arith_expr,
                self.parse_plus_op,
                self.parse_term,
            ]),
        ])(input, pos)
        root.children.append(node)
        return root

    def parse_expr(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("expr")
        node = self.anyof([
            self.parse_arith_expr,
            self.a([
                self.parse_arith_expr,
                self.parse_rel_op,
                self.parse_arith_expr,
            ]),
        ])(input, pos)
        root.children.append(node)
        return root

    def parse_operator(self, input, pos) -> Result[ASTNode, str]:
        root = ASTNode("operator")

        mb_var_node = self.parse_var(input, pos)
        match mb_var_node:
            case Ok(var_node):
                root.children.append(var_node)
            case Err(err):
                return Err(err)
        token = input[pos]
        pos += 1
        if token == "=":
            eq_node = ASTNode("=")
            root.children.append(eq_node)
        mb_expr_node = self.parse_expr(input, pos)
        match mb_expr_node:
            case Ok(expr_node):
                root.children.append(expr_node)
            case Err(err):
                return Err(err)
        return root

    def parse_sep(self, input) -> Result[ASTNode, str]:
        root = ASTNode("sep")
        token = next(input)
        if token in self.plus_ops:
            plus_op_node = ASTNode(token)
            root.children.append(plus_op_node)
        return root

    def parse_operator_list(self, input, pos):
        root = ASTNode("operator_list")
        node = self.anyof([
            self.parse_operator,
            self.a([
                self.parse_operator_list,
                self.parse_sep,
                self.parse_operator
            ]),
        ])(input, pos)
        root.children.append(node)
        return root

    def parse_block(self, input, pos) -> ASTNode:
        root = ASTNode("block")

        term = input[pos]
        pos += 1
        match term:
            case Token(name='BEGIN'):
                root.children.append(ASTNode("begin"))
            case _:
                pass
        opearator_list_node = self.parse_operator_list(input, pos)
        root.children.append(opearator_list_node)
        pos += 1
        match term:
            case Token(name='end'):
                root.children.append(ASTNode("end"))
            case _:
                pass

        return root

    def parse_program(self, input, pos) -> ASTNode:
        root = ASTNode("program")
        block_node = self.parse_block(input, pos)
        root.children.append(block_node)
        return root

    def parse(self, text):
        input = list(PascalLexer(self.patterns).lex(text))
        pos = 0

        root = None
        try:
            root = ASTNode("root")
            program_node = self.parse_program(input, pos)
            root.children.append(program_node)
        except StopIteration:
            pass
        return root
    
    def anyof(self, rules):
        def inner(input, pos):
            for rule in rules:
                node = rule(input, pos)
                if node != None:
                    return node
            return None
        return inner
    
    def a(self, rules):
        def inner(input, pos):
            root = ASTNode("<proxy>")
            for rule in rules:
                node = rule(input, pos)
                if node != None:
                    root.children.append(node)
            return root
        return inner

if __name__ == '__main__':
    example = ""
    with open("examples/example_001.pas", "r") as f:
        example = f.read()
    rules, patterns = read_grammar("grammars/pascal.g")
    parser = PascalParser(patterns)
    ast = parser.parse(example)
    ditree = ast.print()
    print(ditree)
