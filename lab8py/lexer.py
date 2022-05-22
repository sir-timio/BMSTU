
class Position:
    def __init__(self) -> None:
        line = 1
        col = 1
        i = 0
    
    
def lexer(s):
    txt = s.replace('\n', ' ')
    print(txt)
    for c in txt:
        if c == '<':
            



















def main():
    fname = 'input.txt'
    input_text = open(fname, 'r').read()
    lexer(input_text)

if __name__ == '__main__':
    main()