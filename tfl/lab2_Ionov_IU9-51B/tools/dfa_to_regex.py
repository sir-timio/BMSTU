def parse_state(state):
    return ''.join([''.join(s) for s in state])

def dfa_to_regex(dfa):

    states = []
    for s in dfa['states']:
        states.append(parse_state(s))

    alphabet = set(dfa['alphabets'])
    transitions = []
    for state, func in dfa['transition_function'].items():
        for by, to_state in func.items():
            transitions.append([parse_state(state), by, parse_state(to_state)])
    start_state = parse_state(dfa['initial_state'])
    final_states = []
    for fstate in dfa['final_states']:
        final_states.append(parse_state(fstate))
    transitions.append(["start", "ε", start_state[0]])
    final_states = set([f_s for f_s in final_states if f_s in states])
    transitions += [[f_s, "ε", "final"] for f_s in final_states]

    def get_trans_count(states, transitions):
        trans_count = []
        for state in states:
            state_1 = 0
            state_2 = 0
            for transition in transitions:
                if state == transition[0]:
                    state_1 += 1
                elif state == transition[2]:
                    state_2 += 1
            trans_count.append([state, state_1, state_2])
        return trans_count

    def get_from_to_loop_states(transitions, curr_state, alphabet):
        from_states = []
        to_states = []
        loop_states = []
        for transition in transitions:
            begin_state = transition[0]
            end_state = transition[2]
            if curr_state == begin_state and curr_state != end_state:
                from_states.append(transition)
            elif curr_state != begin_state and curr_state == end_state:
                to_states.append(transition)
            elif curr_state == begin_state == end_state:
                loop_states.append(transition)
        state_alphabet = set()
        curr_trans = from_states + loop_states
        for state in curr_trans:
            if state[1] != 'ε':
                state_alphabet.add(state[1])
        return from_states, to_states, loop_states

    trans_count = get_trans_count(states, transitions)
    while len(transitions) != 1 and len(states):
        typed_states = get_from_to_loop_states(transitions, trans_count[0][0], alphabet)
        from_states, to_states, loop_states = typed_states
        single_pass = '+'.join([str(state[1]) for state in loop_states])
        for t_s in to_states:
            for f_s in from_states:
                if len(single_pass) == 0:
                    transitions.append([t_s[0],
                                        str(str(t_s[1]) + str(f_s[1])),
                                        f_s[2]])
                elif len(single_pass) == 1:
                    transitions.append([t_s[0],
                                        str(str(t_s[1]) + str(single_pass) + '*' + str(f_s[1])),
                                        f_s[2]])
                else:
                    transitions.append([t_s[0],
                                        str(str(t_s[1]) + '(' + str(single_pass) + ')*' + str(f_s[1])),
                                        f_s[2]])

        for s in to_states + from_states + loop_states:
            if s in transitions:
                transitions.remove(s)
        states.remove(trans_count[0][0])
        trans_count = get_trans_count(states, transitions)
    regex = '+'.join([str(trans[1]) for trans in transitions])
    return regex