from typing import Any, Dict, FrozenSet, List, Set, Tuple
from itertools import combinations
import json
import copy

# https://github.com/matheuspb/simone

DEAD_STATE = "qdead"


class NFA():
    """
        Non-deterministic finite automaton.
        All operations over automawta are implemented here, this class
        represents a NFA although it can be deterministic. The transition
        function (delta) is represented as a dictionary that maps
        (state, symbol) -> Set[state], it is deterministic if all transitions
        take to only one state.
    """

    def __init__(
            self,
            states: Set[str] = None,
            alphabet: Set[str] = None,
            transitions: Dict[Tuple[str, str], Set[str]] = None,
            initial_state: str = "",
            final_states: Set[str] = None) -> None:
        self._states = states if states else set()
        self._alphabet = alphabet if alphabet else set()
        self._transitions = transitions if transitions else {}
        self._initial_state = initial_state
        self._final_states = final_states if final_states else set()

    @property
    def states(self) -> List[str]:
        """ Returns an ordered list of states """
        return [self._initial_state] + \
               sorted(self._states - {self._initial_state})

    @property
    def alphabet(self) -> List[str]:
        """ Returns an ordered list of symbols """
        return sorted(self._alphabet)

    @property
    def transition_table(self) -> Dict[Tuple[str, str], Set[str]]:
        """ Returns the transition function, a dictionary """
        return self._transitions

    @property
    def initial_state(self) -> str:
        """ Returns the initial state """
        return self._initial_state

    @property
    def final_states(self) -> Set[str]:
        """ Returns the set of final states """
        return self._final_states

    def add_state(self, state: str) -> None:
        """ Adds a state """
        if not self._initial_state:
            self._initial_state = state
        self._states.add(state)

    def remove_state(self, state: str) -> None:
        """ Removes a state """
        # may not remove initial state
        if state != self._initial_state:
            self._states.discard(state)
            self._final_states.discard(state)

            for symbol in self._alphabet:
                # remove useless transitions that come from the removed state
                if (state, symbol) in self._transitions:
                    del self._transitions[state, symbol]

            empty_transitions = set()  # type Set[Tuple[str, str]]
            for actual_state, next_state in self._transitions.items():
                # remove transitions that go to the removed state
                next_state.discard(state)
                if not next_state:
                    empty_transitions.add(actual_state)

            for transition in empty_transitions:
                del self._transitions[transition]

    def toggle_final_state(self, state: str) -> None:
        """ Toggle a state to be final or not """
        if state in self._states:
            if state in self._final_states:
                self._final_states.remove(state)
            else:
                self._final_states.add(state)

    def add_symbol(self, symbol: str) -> None:
        """ Adds a symbol """
        self._alphabet.add(symbol)

    def remove_symbol(self, symbol: str) -> None:
        """ Removes a symbol """
        self._alphabet.discard(symbol)
        for state in self._states:
            # remove transitions by the removed symbol
            if (state, symbol) in self._transitions:
                del self._transitions[state, symbol]

    def set_transition(
            self, state: str, symbol: str, next_states: Set[str]) -> None:
        """ Set the transition function for a given state and symbol """
        if not next_states:
            # assert transition won't exist
            self._transitions.pop((state, symbol), set())
        elif next_states <= self._states:
            self._transitions[state, symbol] = next_states
        else:
            states = ", ".join(next_states - self._states)
            raise KeyError("State(s) {} do not exist".format(states))

    def accept(self, string: str) -> bool:
        """
            Checks if a given string is member of the language recognized by
            the NFA. Using non-deterministic transitions.
        """
        current_state = {self._initial_state}

        for symbol in string:
            next_state = set()  # type Set[str]
            for state in current_state:
                next_state.update(
                    self._transitions.get((state, symbol), set()))
            current_state = next_state

        return bool(current_state.intersection(self._final_states))

    def remove_unreachable(self) -> None:
        """ Removes the states that the automaton will never be in """
        reachable = set()  # type: Set[str]
        new_reachable = {self._initial_state}
        while not new_reachable <= reachable:
            reachable |= new_reachable
            new_reachable_copy = new_reachable.copy()
            new_reachable = set()
            for state in new_reachable_copy:
                for symbol in self._alphabet:
                    new_reachable.update(
                        self._transitions.get((state, symbol), set()))

        for unreachable_state in self._states - reachable:
            self.remove_state(unreachable_state)

    def remove_dead(self) -> None:
        """ Removes states that never reach a final state """
        alive = set()  # type: Set[str]
        new_alive = self._final_states.copy()
        while not new_alive <= alive:
            alive |= new_alive
            new_alive = set()
            for (state, _), next_states in self._transitions.items():
                if any(next_state in alive for next_state in next_states):
                    new_alive.add(state)

        for dead_state in self._states - alive:
            self.remove_state(dead_state)


    @staticmethod
    def from_regular_grammar(grammar) -> 'NFA':
        """ Converts RegularGrammar to NFA """
        initial_symbol = grammar.initial_symbol()
        productions = grammar.productions()

        states = set(productions.keys()) | {"X"}
        alphabet = set()  # type: Set[str]
        transitions = {}  # type: Dict[Tuple[str, str], Set[str]]
        initial_state = initial_symbol
        final_states = set("X") | \
                       ({initial_symbol} if "&" in productions[initial_symbol] else set())

        for non_terminal, prods in productions.items():
            for production in prods:
                if production == "&":
                    continue

                new_transition = "X" if len(production) == 1 else production[1]
                transitions.setdefault(
                    (non_terminal, production[0]), set()).add(new_transition)

                alphabet.add(production[0])

        return NFA(states, alphabet, transitions, initial_state, final_states)
