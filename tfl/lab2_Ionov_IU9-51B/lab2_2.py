import re


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


INCORRECT_SYSTEM_ERROR = 'Некорректная система'
PATH_TO_TEST = 'data/test_2.txt'

LEFT_PR = '('
RIGHT_PR = ')'
STAR = '*'
PLUS = '+'
EQUAL = '='
OR = '|'
VAR_REGEXP = '[A-Z]'
LETTER_REGEXP = '[a-z]'
EOS = '$'

system = []


def is_var(c: str):
    return re.match(VAR_REGEXP, c)


def is_letter(c: str):
    return re.match(LETTER_REGEXP, c)


def parse_expr(q: Queue):
    result = ''
    while is_letter(q.peek()):
        result += q.pop()
    assert result, INCORRECT_SYSTEM_ERROR
    return q, result


def parse_regex(q: Queue):
    if q.peek() == LEFT_PR:
        q.pop()
        exprs = []
        while True:
            q, expr = parse_expr(q)
            exprs.append(expr)
            if q.peek() == OR:
                q.pop()
            else:
                break
        assert q.pop() == RIGHT_PR, INCORRECT_SYSTEM_ERROR
        return q, LEFT_PR + OR.join(exprs) + RIGHT_PR
    else:
        return parse_expr(q)


def parse_system(q: Queue):
    vars_left_side = set()
    vars_right_side = set()
    result = []
    while is_var(q.peek()):
        var = q.pop()
        assert q.pop() == EQUAL, INCORRECT_SYSTEM_ERROR
        line, expression, cur_vars = parse_ar_expr(q)
        vars_right_side |= cur_vars
        result.append([var] + expression)
        vars_left_side.add(var)
        if q.peek() == EOS:
            q.pop()
    assert q.is_empty() and vars_left_side >= vars_right_side, INCORRECT_SYSTEM_ERROR
    return result


def parse_ar_expr(q: Queue):
    vars = set()
    result = []
    while True:
        line, regex = parse_regex(q)
        if is_var(q.peek()):
            var = q.pop()
            vars.add(var)
            result.append([regex, var])
        elif q.is_empty() or q.peek() == EOS:
            result.append([regex, ''])
            return line, result, vars
        else:
            raise Exception(INCORRECT_SYSTEM_ERROR)
        assert q.pop() == PLUS, INCORRECT_SYSTEM_ERROR


def read_txt(path: str) -> str:
    return open(path, 'r').read().replace(' ', '').replace('\n', EOS)


def process_factors(expr: list, target_var: str):
    a, b = [], []
    for t in expr:
        if t[1] == target_var:
            a.append(t[0])
        else:
            b.append(t)
    return a, b


def get_kleene(factors: list):
    if not factors:
        return ''
    if len(factors) == 1 and \
            (len(factors[0]) == 1 or factors[0][0] == LEFT_PR):
        return factors[0] + STAR
    return LEFT_PR + PLUS.join(factors) + RIGHT_PR + STAR


def replace_var(idx):
    global system
    expr = system[idx]
    name = expr[0]
    for i in range(len(system)):
        if i == idx:
            continue
        cur_expr = system[i][1:]
        res_expr = []
        for t in cur_expr:
            if t[1] == name:
                coef = t[0] + expr[1][0]
                res_expr += [[coef + f[0], f[1]] for f in expr[2:]]
            else:
                res_expr.append(t)
        system[i][1:] = res_expr


def set_value(idx):
    global system
    expr = system[idx]
    a = expr[1][0]
    b = expr[2:]
    var_name = expr[0]
    for i in range(idx):
        for j in range(2, len(system[i])):
            cur_expr = system[i][j]
            if cur_expr[1] == var_name:
                system[i][j:j + 1] = [[cur_expr[0] + a + f[0], ''] for f in b]


def solve_system(system):
    print(system)
    eq_amount = len(system)
    for i in range(eq_amount):
        a, b = process_factors(system[i][1:], system[i][0])
        system[i][1:] = [[get_kleene(a), ''], *b]
        replace_var(i)
    for i in range(eq_amount - 1, -1, -1):
        set_value(i)


def format_expression(expr) -> str:
    var_name = expr[0]
    a = expr[1][0]
    b = PLUS.join([t[0] for t in expr[2:]])
    if a == '' or len(expr[2:]) == 1:
        return var_name + EQUAL + a + b
    else:
        return var_name + EQUAL + a + LEFT_PR + b + RIGHT_PR


if __name__ == '__main__':
    system = read_txt(PATH_TO_TEST)
    q = Queue(list(system))
    system = parse_system(q)
    solve_system(system)
    for expr in system:
        print(format_expression(expr))