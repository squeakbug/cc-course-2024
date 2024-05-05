import re
from collections import namedtuple

Token = namedtuple('Token', ('name', 'value'))

class PascalLexer:
    def __init__(self, patterns):
        self.patterns = [
            (re.compile(bytes(p, 'utf8')), name) for p, name in patterns]

    def lex(self, text, ignore_spaces=True):
        self.pos = 0
        self.raw = bytearray(text, 'utf8')
        self.token = ""
        endpos = len(self.raw)

        while self.pos < endpos:
            if ignore_spaces and self.raw[self.pos: self.pos + 1].isspace():
                self.pos += 1
                continue
            for p, name in self.patterns:
                m = p.match(self.raw[self.pos:])
                if m is not None:
                    val, offset = m.group(), m.end()
                    yield Token(name, str(val, 'utf8'))
                    self.pos += offset
                    break
            else:
                self.error('Illegal character')
        yield Token('EOF', None)

    def error(self, message):
        raise SyntaxError(message, self.get_debug_info())

    def get_debug_info(self, f_name=None):
        pos = self.pos + 1
        raw = self.raw
        line_no = raw[:pos].count(b'\n')
        line_start = max(raw.rfind(b'\n'), 0)
        line_end = max(raw.find(b'\n'), len(raw))
        line = str(raw[line_start:line_end], 'utf-8')
        offset = pos - line_start
        return (f_name, line_no, offset, line)


def read_grammar(filename):
    rules, patterns = [], []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if line == "\n":
                break
            else:
                rules.append(line)
        for line in f.readlines():
            left, right = line.strip().split(" = ")
            patterns.append((right, left))
    return rules, patterns


if __name__ == "__main__":
    f = open("examples/example_003.pas")
    example = f.read().strip()
    f.close()
    rules, patterns = read_grammar("grammars/pascal.g")
    print(*[c for c in PascalLexer(patterns).lex(example)], sep="\n")
