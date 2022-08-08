from lab3_Ionov_IU9_51B.uutils import parser as p, tree as t, graph as g

START = 'S'


def checkEntry(suffix: str, word: str, rules: dict, init: str) -> bool:
    if not init:
        return False
    if not suffix:
        return checkEntry(init, word, rules, init) if word else True
    if not word:
        return False

    t = suffix[0]
    if p.is_term(t):
        if word[:1] == t:
            return checkEntry(suffix[1:], word[1:], rules, init)
        return False

    for r in rules[t]:
        if checkEntry(r + suffix[1:], word, rules, init):
            return True

    return False


def get_nterm_term(nterm: str, rules: dict, used: set) -> set:
    res = set()
    if nterm in used:
        return res
    for rule in rules[nterm]:
        words = set("#")
        for term in rule:
            if p.is_term(term):
                tmp = set()
                for w in words:
                    if w == "#":
                        tmp.add(term)
                    else:
                        tmp.add(w + term)
                words = set([t for t in tmp if t != '#'])
            else:
                used.add(nterm)
                suffixes = get_nterm_term(term, rules, used)

                tmp = set()
                for w in words:
                    for s in suffixes:
                        tmp.add(w + s)
                words = tmp

        for w in words:
            res.add(w)
    min_len = -1
    if res:
        min_len = min(len(w) or 0 for w in res)
    return set(
        [w for w in res
         if len(w) == min_len]
    )

def get_reg_closure(rules: dict, reg_nterms: set, possible_reg_nterms: set) -> tuple[set, set]:
    again = 1
    while again:
        again = 0

        for nterm in rules:
            if nterm in reg_nterms or nterm in possible_reg_nterms:
                continue

            is_reg = 1
            is_possible_reg = 1
            for rule in rules[nterm]:
                for term in rule:
                    if p.is_term(term):
                        continue
                    if term not in reg_nterms:
                        is_reg = 0
                        if term not in possible_reg_nterms:
                            is_possible_reg = 0

            if is_reg:
                reg_nterms.add(nterm)
                again = 1
            elif is_possible_reg:
                possible_reg_nterms.add(nterm)
                again = 1
    return reg_nterms, possible_reg_nterms

def analyse(rules: dict):
    graph = g.make_graph(rules)
    reg_nterms = g.get_regular_nterms(rules)
    possible_reg_nterms = set()
    bad_nterms = set()
    pumping_tree = t.get_pumpings(rules)

    for nterm, node in pumping_tree.items():
        if nterm in reg_nterms:
            continue

        pumping = node.get_pumping()
        l, r = pumping.split(nterm, 1)[:2]
        is_reg = 1
        terms = []
        if r:
            terms = p.parse_right(r)

        is_reg = not any([t not in reg_nterms and p.is_nterm(t) for t in terms])

        if not is_reg:
            continue
        if not checkEntry(terms, l, rules, terms):
            bad_nterms.add(nterm)
            continue

        words = get_nterm_term(nterm, rules, set())
        for w in words:
            is_reg *= checkEntry(terms, w, rules, terms)
        if is_reg:
            possible_reg_nterms.add(nterm)

    reg_nterms, possible_reg_nterms = get_reg_closure(rules, reg_nterms, possible_reg_nterms)

    res = ''
    if START in reg_nterms:
        res += 'Regular'
    elif START in possible_reg_nterms:
        res += 'Possible regular'
    elif START in bad_nterms:
        res += 'Suspicious'
    else:
        res += 'Unable to specify'
    res += ' language\n\n'

    res += 'Possible bad nterms: ' + ' '.join(bad_nterms) + '\n'
    res += 'Regular nterms: ' + ' '.join(reg_nterms) + '\n'
    res += 'Possible regular nterms: ' + ' '.join(possible_reg_nterms) + '\n\n'

    for nterm, node in pumping_tree.items():
        if nterm not in reg_nterms:
            label = 0
            tmp, label = node.to_str(label, -1)
            res += tmp + '\n'
    return res
