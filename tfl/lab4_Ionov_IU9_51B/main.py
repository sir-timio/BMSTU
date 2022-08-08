from typing import Dict, Set, List, Tuple
import uuid
import sys

from tools.parser import parse_rules, is_chain, is_term, is_nterm
from tools.lab2 import solve_system

# PATH = 'data/test_1.txt'

START_NTERM = '[S]'
NEW_START_NTERM = '[S*]'
NOT_PRODUCTIVE = 'not productive'
EPS = 'ϵ'


def pretty_print_ds(ds: List[Dict], ls: List[str]):
    for d, l in zip(ds, ls):
        print('\n' + l)
        for k, v in sorted(d.items(), key=lambda x: x[0]):
            print(f'{k}: {v}')
    print()


def main():
    args = sys.argv
    if len(args) != 2:
        print('Usage: main.py <path_to_file>')
    PATH = args[1]
    rules = parse_rules(PATH)
    reg_left, reg_right, reg_closure, reg_iter = get_all_regular_nterms(rules)
    mapping = guard_terms(rules, reg_left | reg_right | reg_iter - reg_closure)
    for nterm, v in mapping.items():
        rules[v] = [[nterm]]
        reg_left.add(v)
        reg_right.add(v)

    # print(f'reg iter: {reg_iter}')
    for s, l in zip([reg_left, reg_right, reg_closure, reg_iter],
                    ['regular left', 'regular right', 'regular closure', 'reg_iter']):
        print(f'{l}: {s}')

    first = get_first_or_last(rules, is_first=True)
    last = get_first_or_last(rules, is_first=False)
    follow = get_follow_or_precede(rules, is_follow=True, subset=first)
    precede = get_follow_or_precede(rules, is_follow=False, subset=last)

    pretty_print_ds([first, last, follow, precede],
                    ['first', 'last', 'follow', 'precede'])

    reg_set = reg_left | reg_right | reg_closure | reg_iter
    tokens = get_tokens(rules, reg_set, follow, precede)
    print(f'tokens: {tokens}')
    regexps = get_regexps(rules, tokens, reg_left, reg_right, reg_closure, reg_iter)
    pretty_print_ds([regexps], ['regexeps'])


def guard_terms(rules: Dict, reg_set: Set) -> Dict:
    def get_guard_name(nterm, term) -> str:
        return f'[Guard_{nterm}_{term}_{str(uuid.uuid4())[:4]}]'


    mapping = dict()
    for nterm in rules.keys():
        if nterm in reg_set:
            continue
        for rule in rules[nterm]:
            for i in range(len(rule)):
                term = rule[i]
                if is_term(term):
                    if term not in mapping.keys():
                        mapping[term] = get_guard_name(nterm, term)
                    rule[i] = mapping[term]
    return mapping


def get_first_or_last(rules: Dict, is_first: bool) -> Dict:
    def get_first_or_last_in_rule(rule: list, is_first: bool) -> str:
        if is_first:
            return rule[0]
        return rule[-1]

    res = dict()
    for nterm, rs in rules.items():
        for rule in rs:
            t = get_first_or_last_in_rule(rule, is_first)
            if is_term(t):
                if nterm not in res:
                    res[nterm] = set()
                res[nterm].add(t)
    while 1:
        leave = 1
        for nterm, rs in rules.items():
            for rule in rs:
                t = get_first_or_last_in_rule(rule, is_first)
                if is_nterm(t):
                    a = res.get(nterm, set())
                    b = res.get(t, set())
                    if b - a:
                        leave = 0
                    res[nterm] = a | b
        if leave:
            break
    return res


def get_follow_or_precede(rules: Dict, subset: Dict, is_follow: bool) -> Dict:
    res = dict()
    if is_follow:
        res[START_NTERM] = set('$')
    else:
        res[START_NTERM] = set('^')

    while 1:
        leave = 1
        for nterm, rs in rules.items():
            for rule in rs:
                for i in range(len(rule)):
                    term = rule[i]
                    if is_term(term):
                        continue
                    a = res.get(term, set())
                    if is_follow:
                        ind = i + 1
                    else:
                        ind = i - 1
                    if (is_follow and i == len(rule) - 1) or (not is_follow and i == 0):
                        b = res.get(nterm, set())
                    elif is_term(rule[ind]):
                        b = set(rule[ind])
                    else:
                        b = subset.get(rule[ind], set())
                    if b - a:
                        leave = 0
                    res[term] = a | b
        if leave:
            break
    return res


def produce_terms(rules: Dict, nterm: str, visited: Set) -> Set:
    res = set()
    for rule in rules.get(nterm, []):
        if len(rule) == 1:
            t = rule[0]
            if is_term(t):
                res.add(t)
            elif t not in visited:
                visited.add(nterm)
                res |= produce_terms(rules, t, visited)
    return res


def get_tokens(rules: Dict, reg_set, follow, precede) -> Set:
    res = set()
    for nterm in reg_set:
        terms = follow.get(nterm, set()) | precede.get(nterm, set())
        produces = produce_terms(rules, nterm, set())
        conflict = terms.intersection(produces)
        if conflict:
            print(f'conflict for nterm: {nterm} and terms: {conflict}')
        else:
            res.add(nterm)
    return res


def get_regexps(rules: Dict, tokens: Set, reg_left: Set, reg_right: Set, reg_closure: Set, reg_iter: Set) -> Dict:
    res = dict()
    productive = get_productive_nterms(rules)
    eqs = build_equations(rules, productive)
    solution = solve_system(eqs)

    for nterm in reg_right - reg_closure:
        if nterm in productive:
            res[nterm] = solution[nterm]
        elif nterm not in reg_iter:
            res[nterm] = NOT_PRODUCTIVE

    left_processed = set()
    for nterm in reg_left - reg_right:
        if nterm in productive:
            grammar = dict()
            left_to_right_grammar(nterm, rules, grammar, start=nterm)
            left_productive = get_productive_nterms(grammar)
            l_solution = solve_system(
                build_equations(grammar,
                                grammar.keys() & left_productive)
            )
            res[nterm] = l_solution.get(NEW_START_NTERM, NOT_PRODUCTIVE)
            left_processed.add(nterm)
        elif nterm not in reg_iter:
            res[nterm] = NOT_PRODUCTIVE

    for nterm in reg_closure:
        if nterm in productive and nterm not in res.keys():
            find_closure_regexps(rules, nterm, productive, res)
        else:
            res[nterm] = NOT_PRODUCTIVE

    again = 1
    while again:
        again = 0
        for nterm in reg_iter - reg_closure - reg_right:
            is_left = 0
            terms = set()
            if nterm in left_processed:
                continue
            for rule in rules[nterm]:
                if is_right_reg(rule):
                    if len(rule) == 2 and rule[1] in res.keys():
                        terms.add(rule[1])
                        again = 0
                    continue
                elif is_left_reg(rule):
                    if rule[0] in res.keys():
                        terms.add(rule[0])
                        again = 1
                    is_left = 1
            if is_left:
                if terms:
                    regexeps = [res[n] for n in terms if n in res.keys()]
                    grammar = dict()
                    left_to_right_grammar(nterm, rules, grammar, start=nterm)
                    left_productive = get_productive_nterms(grammar)
                    l_eqs = build_equations(grammar, grammar.keys() & left_productive)
                    l_solution = solve_system(l_eqs)
                    reg = f'({l_solution.get(nterm, "")})'
                    if reg:
                        regexeps.insert(0, reg)
                    res[nterm] = '+'.join(regexeps)
                    left_processed.add(nterm)
                    again = 1

            iter_eqs = build_equations(rules, reg_iter)
            for i, eq in enumerate(iter_eqs):
                if eq[0] in res.keys() and eq[0] in left_processed:
                    iter_eqs[i] = [eq[0], [f'({res[eq[0]]})', '']]
                    again = 1
                    # if len(iter_eqs[i]) > 1:
                    #     if iter_eqs[i][1][1] == '' or iter_eqs[i][1][1] in res.keys():
                    #         # iter_eqs[i][1] = [f'({res[eq[0]]})', '']
                    #         iter_eqs[i] = [eq[0], [f'({res[eq[0]]})', '']]
                    # else:
                    #     iter_eqs[i] = [eq[0], [f'({res[eq[0]]})', '']]
                    # again = 1
            # print(iter_eqs)
            iter_solution = solve_system(iter_eqs)
            if nterm in productive and nterm not in left_processed:
                if nterm not in res.keys():
                    res[nterm] = iter_solution[nterm]
                left_processed.add(nterm)
                again = 1
            else:
                again = 0

    res = dict({
        token: res.get(token, 'not found') for token in tokens
    })
    return res


def left_to_right_grammar(nterm: str, rules: Dict, grammar: Dict[str, List], start: str, visited=None):
    if visited is None:
        visited = set()
    if nterm in visited:
        return
    for rule in rules.get(nterm, []):
        if len(rule) == 1:
            term = rule[0]
            if is_term(term):
                if NEW_START_NTERM not in grammar:
                    grammar[NEW_START_NTERM] = []
                grammar[NEW_START_NTERM].append([term, nterm])
                if nterm == start:
                    grammar[NEW_START_NTERM].append([term])
            elif is_nterm(term):
                visited.add(nterm)
                left_to_right_grammar(term, rules, grammar, start, visited=visited)
                if term not in grammar:
                    grammar[term] = []
                grammar[term].append([nterm])
        else:
            visited.add(nterm)
            left_to_right_grammar(rule[0], rules, grammar, start, visited)
            if rule[0] not in grammar:
                grammar[rule[0]] = []
            grammar[rule[0]].append([rule[1], nterm])
            if nterm == start:
                grammar[rule[0]].append(rule[1])


def find_closure_regexps(rules: Dict, nterm: str, productive: Set, regexeps: Dict):
    res = ''
    for rule in rules.get(nterm, []):
        c = ''
        add = 1
        for term in rule:
            if is_term(term):
                c += term
            elif term in productive:
                if term not in regexeps:
                    find_closure_regexps(rules, term, productive, regexeps)
                c += regexeps.get(term, '')
            else:
                add = 0
                break

        if add:
            if res == '':
                res = f'({c})'
            else:
                res = f'({res})+({c})'
    regexeps[nterm] = res


def build_equations(rules: Dict, nterms: Set) -> List[Tuple[str, Dict]]:
    res = []
    for nterm in nterms:
        eq = dict()
        for rule in rules.get(nterm, []):
            if len(rule) == 1:
                if is_term(rule[0]):
                    eq['-'] = add_alternative(escape(rule[0]), eq.get('-', ''))
                elif rule[0] in nterms:
                    # eq[rule[0]] = add_alternative(EPS, eq.get(rule[0], ''))
                    eq[rule[0]] = eq.get(rule[0], '')
            elif rule[1] in nterms:
                eq[rule[1]] = add_alternative(escape(rule[0]), eq.get(rule[1], ''))
        eq_list = [nterm]
        for k, v in eq.items():
            if k == '-':
                e = [v, '']
            else:
                e = [v, k]
            eq_list.append(e)
        res.append(eq_list)
    return res


def add_alternative(term: str, c: str = '') -> str:
    if c == '':
        return term
    if len(c) == 1:
        return f'({c}|{term})'
    return f'({c[1:-1]}|{term})'


def escape(s: str) -> str:
    if s in ['(', ')', '*', '+', '$', ]:
        return f'(\\{s})'
    return s


def get_productive_nterms(rules: Dict) -> Set:
    res = set()
    while 1:
        leave = 1
        for nterm, rs in rules.items():
            for rule in rs:
                is_prod = 1
                for term in rule:
                    is_prod *= is_term(term) or term in res
                if is_prod and nterm not in res:
                    leave = 0
                    res.add(nterm)
        if leave:
            break
    return res

from typing import (
    Dict,
    List,
    Set,
)


LEFT = 'L'
RIGHT = 'R'
CLOSURE = 'C'


def make_graph(rules: Dict) -> Dict:
    graph = dict()
    for nterm, rs in rules.items():
        graph[nterm] = [t for r in rs for t in r if not t.islower()]
    return graph


def get_nterms(graph: Dict) -> List:
    nterms = list()
    for nterm, rs in graph.items():
        nterms.append(nterm)
        nterms.extend(rs)
    return sorted(set(nterms))


def is_right_reg(rule: list) -> bool:
    if len(rule) == 1:
        return is_term(rule[0])
    if len(rule) == 2:
        return is_term(rule[0]) and is_nterm(rule[1])
    return False


def is_left_reg(rule: list) -> bool:
    return is_right_reg(list(reversed(rule)))


def get_irregular_nterms(rules: Dict, flag: str) -> List:
    res = set()
    for nterm, rs in rules.items():
        for rule in rs:
            if not (is_chain(rule)
                    or (flag == LEFT and is_left_reg(rule))
                    or (flag == RIGHT and is_right_reg(rule))):
                res.add(nterm)
    return res


def get_reg_nterms(rules: Dict, flag: str) -> set:
    rgraph = reverse_graph(make_graph(rules))
    irr_nterms = get_irregular_nterms(rules, flag)
    visited = set()
    for nterm in irr_nterms:
        dfs(nterm, rgraph, visited)
    res = rules.keys() - visited
    return res


def dfs(node: str, graph: Dict, visited: set):
    if node not in visited:
        visited.add(node)
        for neighbour in graph.get(node, []):
            dfs(neighbour, graph, visited)


def get_all_regular_nterms(rules: Dict) -> list:
    reg_left = get_reg_nterms(rules, LEFT)
    reg_right = get_reg_nterms(rules, RIGHT)

    reg_closure = set()
    again = 1
    while again:
        again = 0
        for nterm in rules.keys():
            reg_nterms = reg_left | reg_right | reg_closure
            if nterm in reg_nterms:
                continue
            is_reg = 1
            for rule in rules[nterm]:
                for term in rule:
                    is_reg *= is_term(term) or term in reg_nterms
            if is_reg:
                reg_closure.add(nterm)
                again = 1

    reg_iter = set()
    # reg_iter = get_reg_iter(rules)
    # CHANGE TO DEFAULT
    return reg_left, reg_right, reg_closure, reg_iter


def get_reg_iter(rules) -> Set:
    reg_iter = set()
    reg_left = set()
    reg_right = set()
    not_reg_linear = set()
    again = 1
    while again:
        again = 0
        reg_iter = reg_iter | reg_left | reg_right
        for nterm, rs in rules.items():
            if nterm in reg_iter:
                continue
            if nterm in not_reg_linear:
                continue
            for rule in rs:
                if len(rule) == 1:
                    if is_term(rule[0]) or (is_nterm(rule[0]) and rule[0] in reg_iter):
                        reg_iter.add(nterm)
                        again = 1
                elif is_left_reg(rule) and rule[0] in reg_iter:
                    reg_left.add(nterm)
                    again = 1
                elif is_right_reg(rule) and rule[1] in reg_iter:
                    reg_right.add(nterm)
                    again = 1
                elif not (is_left_reg(rule) or is_right_reg(rule)):
                    not_reg_linear.add(nterm)
                    if nterm in reg_iter:
                        reg_iter.remove(nterm)
                    again = 1
                else:
                    again = 0
    return reg_iter


def reverse_graph(graph: Dict) -> Dict:
    reversed_graph = dict()

    for nterm, rs in graph.items():
        for r in rs:
            if r not in reversed_graph.keys():
                reversed_graph[r] = list()
            reversed_graph[r].append(nterm)
    return reversed_graph


if __name__ == '__main__':
    main()
