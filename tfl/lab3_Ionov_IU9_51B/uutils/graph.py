import re
from typing import (
    Dict,
    List,
    Set
)

NTERM_REGEX = '[A-Z][0-9]*'
LETTER_REGEX = '[a-z]'
REGULAR_REGEX = f'{LETTER_REGEX}({NTERM_REGEX})?'


def is_regular(rs: List) -> bool:
    r = ''.join(rs)
    return re.fullmatch(REGULAR_REGEX, r)


def make_graph(rules: Dict) -> Dict:
    graph = dict()
    for nterm, rs in rules.items():
        graph[nterm] = [t for r in rs for t in r if not t.islower()]
    return graph


def get_reachable(graph: Dict) -> List:
    visited = list()

    def dfs(node: str):
        nonlocal visited, graph

        if node not in graph:
            return

        if node not in visited:
            visited.append(node)
            for neighbour in graph[node]:
                dfs(neighbour)

    dfs("S")
    return visited


def get_nterms(graph: Dict) -> set:
    nterms = list()
    for nterm, rs in graph.items():
        nterms.append(nterm)
        nterms.extend(rs)
    return set(nterms)


def get_irregular_nterms(rules: Dict) -> set:
    irr_nterms = set()

    for nterm, rs in rules.items():
        for rule in rs:
            if not is_regular(rule):
                irr_nterms.add(nterm)
    return irr_nterms

def dfs(node: str, graph: Dict, visited: set):
    if node not in visited:
        visited.add(node)
        for neighbour in graph.get(node, []):
            dfs(neighbour, graph, visited)


def get_regular_nterms(rules) -> set:
    nterms = get_nterms(make_graph(rules))
    irr_nterms = get_irregular_nterms(rules)
    rgraph = reverse_graph(make_graph(rules))

    visited = set()
    for nterm in irr_nterms:
        dfs(nterm, rgraph, visited)
    return nterms - visited


def reverse_graph(graph: Dict) -> Dict:
    reversed_graph = dict()

    for nterm, rs in graph.items():
        for r in rs:
            if r not in reversed_graph.keys():
                reversed_graph[r] = list()
            reversed_graph[r].append(nterm)
    return reversed_graph
