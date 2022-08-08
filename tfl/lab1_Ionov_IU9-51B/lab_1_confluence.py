def prefix(s: str) -> list:
    pref = [0 for _ in range(len(s))]
    j = 0
    i = 1
    while i < len(s):
        if s[j] != s[i]:
            if j > 0:
                j = pref[j - 1]
            else:
                i += 1
        else:
            pref[i] = j + 1
            i += 1
            j += 1

    return pref


def is_overlap(s1: str, s2: str) -> int:
    return prefix(s1 + '#' + s2)[-1]


def read_txt(path: str) -> list:
    return open(path, 'r').read().split('\n')


def find_confluence_term(rules: list) -> str:
    rules_amount = len(rules)
    for i in range(rules_amount):
        for j in range(rules_amount):
            if i == j:
                if prefix(rules[i])[-1]:
                    return f'{rules[i]}'
            elif is_overlap(rules[i], rules[j]):
                return f'{rules[i]} c  {rules[j]}'
    return ''

def check_confluence(lines):
    length = len(lines)
    for i in range(length):
        for j in range(length):
            if i == j:
                if prefix(lines[i])[-1]:
                    return [lines[i]]
            elif prefix(lines[i] + '#' + lines[j])[-1]:
                return [lines[i], lines[j]]
    return []


def main() -> None:
    input_path = 'rules.txt'
    rules = read_txt(input_path)
    rules_left = [r.replace(' ', '').split('->')[0] for r in rules]
    term = find_confluence_term(rules_left)
    no_conf_verdict = 'система, возможно, неконфлюэнтна, перекрытие внутри терма'
    if term:
        print(no_conf_verdict + ' ' + term)
    else:
        print('система конфлюента')


if __name__ == '__main__':
    main()
