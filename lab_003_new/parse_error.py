class ParseError(Exception):
    def __init__(self, pos, lexem) -> None:
        self.pos = pos
        self.term = lexem

    def __str__(self) -> str:
        return super().__str__() + f" at position {self.pos}:\n{self.term}"
