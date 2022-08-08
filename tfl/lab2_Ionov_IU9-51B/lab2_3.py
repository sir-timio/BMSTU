from tools.RegularGrammar import RegularGrammar
from tools.NFA import NFA
from tools.nfa_to_dfa import nfa_to_dfa
from tools.dfa_to_regex import dfa_to_regex

# Z -> aS
# Z->aA
# Z->a
# A->eS
# S -> aZ
# A -> bQ
# Q -> kV
# V -> aQ
# S -> cS
# S ->aA
# S -> y
# S -> z

import re

PATH_TO_TEST = 'data/test_3.txt'
EPS = ''
TRANSITION = '->'
OR = '|'
INCORRECT_SYSTEM_ERROR = 'Некорректная система'
INCORRECT_SYNTAX_ERROR = 'Синтаксическая ошибка'
RULE_REGEX = '[A-Z]->[a-z][A-Z]?'
graph_map = dict()


def read_txt(path: str) -> str:
    return open(path, 'r').read().replace(' ', '').split('\n')


class Graph:
    def __init__(self, state):
        self.state = state
        self.edges = []

    def set_edge(self, by, to_state=EPS):
        self.edges.append((by, to_state))

    def __str__(self):
        self.edges.sort(key=lambda x: x[1], reverse=True)
        return self.state + TRANSITION + OR.join(
            [e[0] + e[1] for e in self.edges]
        )

    def get_edges(self):
        return set(e[0] + e[1] for e in self.edges)


def graph_map_to_rg_constructor():
    global graph_map
    const = dict()
    for state, graph in graph_map.items():
        const[state] = graph.get_edges()
    return const


def rule_to_graph(rule: str) -> Graph:
    global graph_map
    state, tail = rule.split(TRANSITION)

    if state not in graph_map.keys():
        graph = Graph(state)
        graph_map[state] = graph
    graph = graph_map[state]
    assert len(tail), INCORRECT_SYSTEM_ERROR
    by = tail[0]
    to_state = tail[1:] if len(tail) > 1 else EPS
    graph.set_edge(by, to_state)
    return graph


def check_states():
    for g in graph_map.values():
        for t in g.get_edges():
            if len(t) > 1 and t[1] not in graph_map.keys():
                return False
    return True


# S -> bN
# S -> aM
# S -> b
# N -> aL
# L -> aN
# M -> aS

# (a(aa)*ab|b)


if __name__ == '__main__':
    rules = read_txt(PATH_TO_TEST)
    graphs = []
    for r in rules:
        assert re.fullmatch(RULE_REGEX, r), INCORRECT_SYNTAX_ERROR
        graphs.append(rule_to_graph(r))
    assert check_states(), INCORRECT_SYSTEM_ERROR

    const = graph_map_to_rg_constructor()
    rg = RegularGrammar('S', const)
    nfa_from_rg = NFA.from_regular_grammar(rg)
    dfa = nfa_to_dfa(nfa_from_rg, minimize_flag=1)
    regex = dfa_to_regex(dfa)
    print(regex)
