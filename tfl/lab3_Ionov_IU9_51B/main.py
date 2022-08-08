from uutils import parser as p
from uutils import analytics as a

PATH_TO_TEST = 'data/test_1.txt'


def main():
    rules = p.parse_rules(PATH_TO_TEST)
    res = a.analyse(rules)
    print(res)


if __name__ == '__main__':
    main()
