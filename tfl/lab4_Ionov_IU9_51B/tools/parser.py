import re
from typing import Dict

INCORRECT_SYNTAX_ERROR = 'Синтаксическая ошибка'

EPS = ''
SEP = '::='
OR = '|'
TERM_REGEX = '[a-z]|[0-9]|_|\*|\+|=|\(|\)|\$|;|:'
NTERM_REGEX = '\[[A-Za-z]+\]'
LETTER_REGEX = '[a-z]'
DIGIT_REGEX = '[0-9]'


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
    return bool(re.fullmatch(NTERM_REGEX, s)) or s.startswith('[Guard')


def is_term(s: str):
    return bool(re.fullmatch(TERM_REGEX, s))


def is_chain(rule: list) -> bool:
    return len(rule) == 1 and is_nterm(rule[0])


def read_txt(path: str) -> str:
    raw_rules = open(path, 'r').read().replace(' ', '').split('\n')
    raw_rules[:] = [r for r in raw_rules if r]
    return raw_rules


def parse_right(q: Queue) -> list:
    if isinstance(q, str):
        q = Queue(q)
    res = []
    nterm = ''
    while not q.is_empty():
        if q.peek() == '[':
            while q.peek() != ']':
              nterm += q.pop()
            nterm += q.pop()
            res.append(nterm)
            nterm = ''
        else:
            res.append(q.pop())
        assert INCORRECT_SYNTAX_ERROR
    assert len(res), INCORRECT_SYNTAX_ERROR
    return res


def parse_rules(path: str) -> Dict:
    raw_rules = read_txt(path)
    rules = dict()
    for r in raw_rules:
        left, right = r.split(SEP)[:2]
        if not is_nterm(left):
            assert INCORRECT_SYNTAX_ERROR
        if left not in rules.keys():
            rules[left] = list()
        q = Queue(right)
        rules[left].append(parse_right(q))
    return rules

