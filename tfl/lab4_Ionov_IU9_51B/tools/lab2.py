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
    if ''.join(factors) == '':
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


def solve_system(sys) -> dict:
    global system
    system = sys
    eq_amount = len(system)
    for i in range(eq_amount):
        a, b = process_factors(system[i][1:], system[i][0])
        system[i][1:] = [[get_kleene(a), ''], *b]
        replace_var(i)
    for i in range(eq_amount - 1, -1, -1):
        set_value(i)
    answer = dict()
    for expr in system:
        l, r = format_expression(expr).split(EQUAL, 1)
        answer[l] = r
    return answer


def format_expression(expr) -> str:
    var_name = expr[0]
    a = expr[1][0]
    b = PLUS.join([t[0] for t in expr[2:]])
    if a == '' or len(expr[2:]) == 1:
        return var_name + EQUAL + a + b
    else:
        return var_name + EQUAL + a + LEFT_PR + b + RIGHT_PR