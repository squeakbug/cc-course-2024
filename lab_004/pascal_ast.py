from graphviz import Digraph

class ASTNode:
    def __init__(self, data, value=None) -> None:
        self.data = data
        self.value = value
        self.children = []

    def print(self, tree = None, parent="", id = "main"):
        if not tree:
            tree = Digraph()
            tree.node_attr["shape"] = "plain"
        tree.node(id, "%s" % str(self.value))
        if parent:
            tree.edge(parent, id)
        for i, child in enumerate(self.children):
            child.print(tree, id, id + "." + str(i))
        return tree