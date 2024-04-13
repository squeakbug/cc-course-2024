import os.path
import argparse

from graphviz import Digraph

import grammar_converter as grammar_converter


class Node:
    """
    Используется для хранения информации о символе грамматики. 
    У узла может быть максимум два дочерних элемента, поскольку грамматика в нормальной форме Хомского.

    1) child1 - терминальный символ-строка
    2) child1, child2 - нетерминальные символы грамматики
    """

    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        return self.symbol


class Parser:
    def __init__(self, grammar, sentence):
        self.parse_table = None
        self.prods = {}
        self.grammar = None
        if os.path.isfile(grammar):
            self.grammar_from_file(grammar)
        else:
            self.grammar_from_string(grammar)
        self.__call__(sentence)

    def __call__(self, sentence, parse=False):
        if os.path.isfile(sentence):
            with open(sentence) as inp:
                self.input = inp.readline().split()
                if parse:
                    self.parse()
        else:
            self.input = sentence.split()

    def grammar_from_file(self, grammar):
        self.grammar = grammar_converter.convert_grammar_to_cnf(grammar_converter.read_grammar(grammar))

    def grammar_from_string(self, grammar):
        self.grammar = grammar_converter.convert_grammar_to_cnf([x.replace("->", "").split() for x in grammar.split("\n")])

    def parse(self):
        length = len(self.input)

        self.parse_table = [[[] for x in range(length - y)] for y in range(length)]

        for i, word in enumerate(self.input):
            for rule in self.grammar:
                if f"'{word}'" == rule[1]:
                    self.parse_table[0][i].append(Node(rule[0], word))

        for k in range(1, length):
            for starting_cell in range(0, length - k):
                for left_size in range(1, k + 1):
                    right_size = k - left_size + 1

                    left_cell = self.parse_table[left_size - 1][starting_cell]
                    right_cell = self.parse_table[right_size - 1][starting_cell + left_size]

                    for rule in self.grammar:
                        left_nodes = [n for n in left_cell if n.symbol == rule[1]]
                        if left_nodes:
                            right_nodes = [n for n in right_cell if n.symbol == rule[2]]
                            self.parse_table[k][starting_cell].extend(
                                [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                            )


    def print_tree(self, output=True):
        start_symbol = self.grammar[0][0]
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
        if final_nodes:
            if output:
                print("Заданная цепочка принадлежим языку, порождаемому данной грамматикой!")
                print("\nВозможные разборы цепочки символов:")
            trees = [generate_tree(node) for node in final_nodes]
            if output:
                for tree in trees:
                    print("=" * 80)
                    print(tree)
            else:
                return trees
        else:
            print("Заданная цепочка НЕ принадлежим языку, порождаемому данной грамматикой!")


def generate_tree(node, tree = None, id = "main", level=1):
    if level == 1:
        tree = Digraph()
        tree.node_attr["shape"] = "plain"

    if node.child2 is None:
        tree.node(id, node.symbol)
        tree.node(f"{id}.{node.symbol}", node.child1)
        tree.edge(id, f"{id}.{node.symbol}")
    else:
        generate_tree(node.child1, tree, f"{id}.{node.child1.symbol}", level+1)
        generate_tree(node.child2, tree, f"{id}.{node.child2.symbol}", level+1)
        tree.node(f"{id}.{node.child1.symbol}", node.child1.symbol)
        tree.node(f"{id}.{node.child2.symbol}", node.child2.symbol)
        tree.edge(id, f"{id}.{node.child1.symbol}")
        tree.edge(id, f"{id}.{node.child2.symbol}")
    return tree


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("grammar",
                           help="Файл, содержащий описание грамматики или строка, содержащая описание грамматики.")
    argparser.add_argument("sentence",
                           help="Файл, содержащий входную цепочку или строка, содержащая входную цепочку.")
    args = argparser.parse_args()
    CYK = Parser(args.grammar, args.sentence)
    CYK.parse()
    CYK.print_tree()