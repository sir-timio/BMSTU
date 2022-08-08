import re
from typing import List, Dict

EPS = ''
SEP = '->'
OR = '|'
NTERM_REGEX = '[A-Z][0-9]*'
LETTER_REGEX = '[a-z]'
DIGIT_REGEX = '[0-9]'
TERM_REGEX = f'({NTERM_REGEX})|{LETTER_REGEX})'
RULE_REGEX = f'({NTERM_REGEX}->{LETTER_REGEX}({TERM_REGEX}*)'

INCORRECT_SYNTAX_ERROR = 'Синтаксическая ошибка'

class Queue(list):
    def __init__(self, *args):
        super().__init__(*args)

    def peek(self):
        item = ''
        try:
            item = self.__getitem__(0)
        finally:
            return item

    def is_empty(self):
        return not len(self)

    def pop(self, **kwargs):
        item = ''
        try:
            item = super().pop(0)
        finally:
            return item


def is_nterm(s: str) -> bool:
    return bool(re.fullmatch(NTERM_REGEX, s))


def is_digit(s: str) -> bool:
    return bool(re.fullmatch(DIGIT_REGEX, s))


def is_term(s: str) -> bool:
    return len(s) == 1 and s.islower()


def is_upper(s: str) -> bool:
    return s.isupper()


def parse_right(s: str) -> List:
    q = Queue(s)
    res = []
    while not q.is_empty():
        if is_term(q.peek()):
            res.append(q.pop())
        elif is_upper(q.peek()):
            nterm = q.pop()
            while is_digit(q.peek()):
                nterm += q.pop()
            res.append(nterm)
        assert INCORRECT_SYNTAX_ERROR
    assert len(res), INCORRECT_SYNTAX_ERROR
    return res


def read_txt(path: str) -> str:
    raw_rules = open(path, 'r').read().replace(' ', '').replace('\t', '').split('\n')
    raw_rules = [r for r in raw_rules if r]

    return raw_rules


def parse_rules(path: str) -> Dict:
    raw_rules = read_txt(path)
    rules = dict()
    for r in raw_rules:
        assert re.fullmatch(RULE_REGEX, r), INCORRECT_SYNTAX_ERROR
        left, right = r.split(SEP)[:2]
        if left not in rules.keys():
            rules[left] = list()

        rules[left].append(parse_right(right))
    return rules
