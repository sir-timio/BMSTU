import re


class Term:
    def __init__(self, type, name, args):
        self.type = type
        self.name = name
        self.args = args

    def __str__(self):
        res = self.name
        if self.type != 'const' and self.type != 'var':
            res += '('
            for arg in self.args:
                res += str(arg) + ','
            res = res[:-1] + ')'
        return res


def get_constructors_and_consts(line):
    constructors = line.replace('constructors=', '')
    func = {}
    const = []
    for cons in constructors.split(','):
        num = int(cons[2:-1])
        if num == 0:
            const.append(cons[0])
        else:
            func[cons[0]] = int(num)
    return func, const


def get_vars(line):
    variables = line.replace('variables=', '')
    return variables.split(',')


def get_term(line, constructors, consts, vars):
    def pop_next():
        nonlocal curr_pos
        curr_pos += 1
        if curr_pos < len(term):
            return term[curr_pos]

    def parse_term(num_args):
        res = []
        while True:
            curr_char = pop_next()
            if curr_char in constructors:
                if pop_next() == '(':
                    constr_args = parse_term(constructors[curr_char])
                    if not constr_args or pop_next() != ')':
                        return
                    res.append(Term('constr', curr_char, constr_args))
                else:
                    return
            elif curr_char in vars:
                res.append(Term('var', curr_char))
            elif curr_char in consts:
                res.append(Term('const', curr_char))
            else:
                return
            num_args -= 1
            if num_args == 0:
                return res
            curr_char = pop_next()
            if curr_char != ',':
                break
        return None if curr_char else res

    term = re.sub(r'first=|second=', '', line)
    curr_pos = -1
    parse_term = parse_term(1)
    return parse_term[0] if parse_term and curr_pos + 1 == len(term) else None


def unification(term1, term2):
    if term1.type == 'var':
        return term2, [f'{term1}:={term2}']
    elif term2.type == 'var':
        return term1, [f'{term2}:={term1}']
    elif term1.type == term2.type:
        if term1.name == term2.name:
            args = []
            substs = []
            for i in range(len(term1.args)):
                unific_res = unification(term1.args[i], term2.args[i])
                if not unific_res:
                    return
                args.append(unific_res[0])
                substs.extend(unific_res[1])
            return Term(term1.type, term1.name, args), substs


if __name__ == '__main__':
    with open('test_1.txt') as file:
        lines = file.readlines()
        lines = [re.sub(r'[ |\n]+', '', line) for line in lines]
    constructors, consts = get_constructors_and_consts(lines[0])
    vars = get_vars(lines[1])
    first = get_term(lines[2], constructors, consts, vars)
    second = get_term(lines[3], constructors, consts, vars)
    if first and second:
        unification_res = unification(first, second)
        if unification_res:
            for res in unification_res[1]:
                print(res)
            print(unification_res[0])
        else:
            print('невозможно унифицировать')
    else:
        print('не соответствует грамматике')