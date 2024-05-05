class ParseError(Exception):
    def __init__(self, pos, token) -> None:
        self.pos = pos
        self.token = token

    def __str__(self) -> str:
        return super().__str__() + f" at position {self.pos}:\n{self.token}"
