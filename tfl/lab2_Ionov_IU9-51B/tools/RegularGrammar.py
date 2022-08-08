from typing import Dict, Set

# https://github.com/matheuspb/simone

class RegularGrammar():
    """
        For example, the grammar:
        S -> aA | bB | a | b
        A -> aA | a
        B -> bB | b
        is represented as:
        {
            "S": {"aA", "bB", "a", "b"},
            "A": {"aA", "a"},
            "B": {"bB", "b"}
        }
    """

    def __init__(
            self, initial_symbol: str="S",
            productions: Dict[str, Set[str]]=None) -> None:
        self._initial_symbol = initial_symbol
        self._productions = productions if productions else {}

    def initial_symbol(self):
        return self._initial_symbol

    def productions(self):
        return self._productions