import re
import sys


class Token(object):
    def __init__(self, type, val, col, row):
        self.type = type
        self.val = val
        self.col = col
        self.row = row

    def __str__(self):
        return f"{self.type}\t({self.row},{self.col}):\t{self.val}"


class LexerError(Exception):
    def __init__(self, col, row):
        self.col = col
        self.row = row
    def __str__(self) -> str:
        return f"syntax error\t({self.row},{self.col})"


class Lexer(object):

    def __init__(self, rules):
        regex_parts = []

        for regex, type in rules:
            regex_parts.append('(?P<%s>%s)' % (type, regex))

        self.regex = re.compile('|'.join(regex_parts))
        self.ws_re = re.compile('\S')

    def input(self, buf, row):
        self.buf = buf
        self.col = 0
        self.row = row

    def token(self):
        if self.col >= len(self.buf):
            return None
        m = self.ws_re.search(self.buf, self.col)

        if m:
            self.col = m.start()
        else:
            return None

        m = self.regex.match(self.buf, self.col)
        if m:
            tok_type =  m.lastgroup
            tok = Token(tok_type, m.group(tok_type), self.col, self.row)
            self.col = m.end()
            return tok

        raise LexerError(self.col, self.row)

    def tokens(self):
        """ Returns an iterator to the tokens found in the buffer.
        """
        while 1:
            token = self.token()
            if token is None: break
            yield token


if __name__ == '__main__':

    VOWELS = "[aeiou]"
    CONS = "[b-df-hj-np-tv-z]"
    IDENT = "\\b((0(10)*1?)|(1(01)*0?))\\b".\
            replace("0", CONS).replace("1", VOWELS)
    NUMBER = "\\b(1(0+1?)*)|0\\b"
    
    rules = [
        (NUMBER,   'NUMBER'),
        (IDENT,    'IDENT')
    ]

    lexer = Lexer(rules)
    path = sys.argv[1]
    lines = open(path, 'r').read().split("\n")
    for i, line in enumerate(lines):
        lexer.input(line, i+1)
        try:
            for token in lexer.tokens():
                print(token)
        except LexerError as e:
            print(e)
    