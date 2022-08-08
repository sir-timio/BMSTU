from typing import List
from lab3_Ionov_IU9_51B.uutils.parser import is_term
from lab3_Ionov_IU9_51B.uutils.graph import get_reachable,make_graph

NOPUMP = 0
PUMP = 1


class Node:
    def __init__(self, term: str, pumps: List = None):
        self.term = term
        self.pumps = pumps

    def get_pumping(self):
        if self.pumps:
            return ''.join([n.get_pumping() for n in self.pumps])
        return self.term

    def get_pumps(self):
        return self.pumps or []

    def to_str(self, label, parent_label):
        res = f'\t{label} [label="{self.term}"]\n'
        if parent_label != -1:
            res += f'\t{parent_label} -> {label}\n'
        l = label
        label += 1
        for child in self.get_pumps():
            tmpres, label = child.to_str(label, l)
            res += tmpres
        if parent_label == -1:
            res = f'digraph {self.term}' + ' {\n' + res + '}'
        return res, label

def dfs(node: str, graph: dict, visited: set):
    if node not in visited:
        visited.add(node)
        for neighbour in graph.get(node, []):
            dfs(neighbour, graph, visited)

def pump_nterm(nterm: str, start: str, rules: dict, used: set) -> tuple:

    if is_term(nterm):
        return Node(nterm), NOPUMP

    if nterm in used:
        if nterm == start:
            return Node(nterm), PUMP
        return None, NOPUMP

    for rule in rules[nterm]:
        flag = NOPUMP
        children = []
        for term in rule:
            if flag == PUMP:
                children.append(Node(term))
            else:
                used.add(nterm)
                node, flag = pump_nterm(term, start, rules, used)
                if not node:
                    break
                children.append(node)
        if flag == PUMP:
            return Node(nterm, children), PUMP
    return None, NOPUMP


def get_pumpings(rules) -> dict:
    tree = dict()
    reachable = get_reachable(graph=make_graph(rules))

    for nterm in reachable:
        node, flag = pump_nterm(nterm, nterm, rules, set())
        if flag:
            tree[nterm] = node
    return tree
