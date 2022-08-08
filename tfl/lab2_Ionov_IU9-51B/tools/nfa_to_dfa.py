import itertools
from collections import Counter
EPSILON = '$'

PHI = tuple('Ⴔ', )

# https://github.com/b30wulffz/automata-toolkit


def find_permutation(state_list, current_state):
    for state in state_list:
        if Counter(current_state) == Counter(state):
            return state
    return current_state

def minimize(dfa):
    table = {}
    new_table = {}
    for state in dfa["reachable_states"]:
        table[state] = {}
        new_table[state] = {}
        for again_state in dfa["reachable_states"]:
            table[state][again_state] = 0
            new_table[state][again_state] = 0

    # populate final, non final pairs
    for state in dfa["reachable_states"]:
        if state not in dfa["final_reachable_states"]:
            for again_state in dfa["final_reachable_states"]:
                table[state][again_state] = 1
                new_table[state][again_state] = 1
                table[again_state][state] = 1
                new_table[again_state][state] = 1

    while True:
        for state_1 in dfa["reachable_states"]:
            for state_2 in dfa["reachable_states"]:
                for alphabet in dfa["alphabets"]:
                    # transition for an alphabet
                    if new_table[state_1][state_2] == 0:
                        next_state_1 = dfa["transition_function"][state_1][alphabet]
                        next_state_2 = dfa["transition_function"][state_2][alphabet]
                        new_table[state_1][state_2] = table[next_state_1][next_state_2]
                        new_table[state_2][state_1] = table[next_state_1][next_state_2]
                    else:
                        break

        changed = False
        # check if something changed or not
        for state_1 in dfa["reachable_states"]:
            for state_2 in dfa["reachable_states"]:
                if new_table[state_1][state_2] == 1 and table[state_1][state_2] == 0:
                    table[state_1][state_2] = new_table[state_1][state_2]
                    changed = True
        if not changed:
            break

    # implementing union find to merge
    parent = {}
    for state in dfa["reachable_states"]:
        # parent[state] = state
        parent[state] = {"value": state, "states": [state]}

    def get_parent(current_state, all=False):
        parent_state = parent[current_state]
        while parent_state["value"] != current_state:
            current_state = parent_state["value"]
            parent_state = parent[current_state]
        if all:
            return parent_state
        else:
            return tuple(parent_state["states"])

    for state_1 in dfa["reachable_states"]:
        for state_2 in dfa["reachable_states"]:
            if state_1 != state_2 and table[state_1][state_2] == 0:
                # merge state 1 and 2
                parent_state_1 = get_parent(state_1, all=True)
                parent_state_2 = get_parent(state_2, all=True)
                parent[parent_state_2["value"]]["value"] = parent_state_1["value"]
                parent[parent_state_1["value"]]["states"] = list(
                    set(parent_state_1["states"]) | set(parent_state_2["states"]))

    # now we can create our new dfa
    new_dfa = {}
    new_dfa["states"] = list(set([get_parent(state) for state in dfa["reachable_states"]]))
    new_dfa["initial_state"] = get_parent(dfa["initial_state"])
    new_dfa["final_states"] = list(set([get_parent(state) for state in dfa["final_reachable_states"]]))
    # new_dfa["alphabets"] = ["a", "b"]
    new_dfa["alphabets"] = dfa["alphabets"]

    new_dfa["transition_function"] = {}
    for state in new_dfa["states"]:
        new_dfa["transition_function"][state] = {}
        for alphabet in new_dfa["alphabets"]:
            new_dfa["transition_function"][state][alphabet] = get_parent(dfa["transition_function"][state[0]][alphabet])

    # extras
    new_dfa["reachable_states"] = new_dfa["states"]
    new_dfa["final_reachable_states"] = new_dfa["final_states"]
    return new_dfa

def get_epsilon_closure(nfa, dfa_states, state):
    closure_states = []
    state_stack = [state]
    while len(state_stack) > 0:
        current_state = state_stack.pop(0)
        closure_states.append(current_state)
        alphabet = EPSILON
        if nfa["transition_function"][current_state][alphabet] not in closure_states:
            state_stack.extend(nfa["transition_function"][current_state][alphabet])
    closure_states = tuple(set(closure_states))
    return find_permutation(dfa_states, closure_states)

def make_nfa_compatible(nfa_from_rg):
    nfa = {}
    nfa["states"] = nfa_from_rg.states
    nfa["initial_state"] = nfa_from_rg.initial_state
    nfa["final_states"] = nfa_from_rg.final_states
    nfa["alphabets"] = nfa_from_rg.alphabet
    nfa["alphabets"].append('$')
    nfa["transition_function"] = {}
    for state in nfa["states"]:
        nfa["transition_function"][state] = {}
        for letter in nfa["alphabets"]:
            nfa["transition_function"][state][letter] = []
    transitions = nfa_from_rg.transition_table
    for from_state, letter in transitions:
        nfa["transition_function"][from_state][letter] = list(transitions[from_state, letter])
    return nfa

def nfa_to_dfa(nfa_, minimize_flag=False):
    nfa = make_nfa_compatible(nfa_)

    dfa = {}

    dfa["states"] = [PHI]
    for r in range(1, len(nfa["states"]) + 1):
        dfa["states"].extend(itertools.combinations(nfa["states"], r))

    # calculate epsilon closure of all states of nfa
    epsilon_closure = {}
    for state in nfa["states"]:
        epsilon_closure[state] = get_epsilon_closure(nfa, dfa["states"], state)
    dfa["initial_state"] = epsilon_closure[nfa["initial_state"]]

    dfa["final_states"] = []
    for state in dfa["states"]:
        if state != PHI:
            for nfa_state in state:
                if nfa_state in nfa["final_states"]:
                    dfa["final_states"].append(state)
                    break

    # dfa["alphabets"] = ["a", "b"]
    dfa["alphabets"] = list(filter(lambda x: x != EPSILON, nfa["alphabets"]))

    dfa["transition_function"] = {}
    for state in dfa["states"]:
        dfa["transition_function"][state] = {}
        for alphabet in dfa["alphabets"]:
            if state == PHI:
                dfa["transition_function"][state][alphabet] = state
            else:
                transition_states = []
                if len(state) == 1:
                    nfa_state = state[0]
                    next_nfa_states = nfa["transition_function"][nfa_state][alphabet]
                    for next_nfa_state in next_nfa_states:
                        transition_states.extend(epsilon_closure[next_nfa_state])
                else:
                    for nfa_state in state:
                        nfa_state = tuple([nfa_state])
                        if dfa["transition_function"][nfa_state][alphabet] != PHI:
                            transition_states.extend(dfa["transition_function"][nfa_state][alphabet])
                transition_states = tuple(set(transition_states))

                if len(transition_states) == 0:
                    dfa["transition_function"][state][alphabet] = PHI
                else:
                    # find permutation of transition states in states
                    dfa["transition_function"][state][alphabet] = find_permutation(dfa["states"], transition_states)

    state_stack = [dfa["initial_state"]]
    dfa["reachable_states"] = []
    while len(state_stack) > 0:
        current_state = state_stack.pop(0)
        if current_state not in dfa["reachable_states"]:
            dfa["reachable_states"].append(current_state)
        for alphabet in dfa["alphabets"]:
            next_state = dfa["transition_function"][current_state][alphabet]
            if next_state not in dfa["reachable_states"]:
                state_stack.append(next_state)

    dfa["final_reachable_states"] = list(set(dfa["final_states"]) & set(dfa["reachable_states"]))
    if minimize_flag:
        dfa = minimize(dfa)
    return dfa
