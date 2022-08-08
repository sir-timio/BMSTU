import json
from collections import namedtuple

Term = namedtuple('term', "type name args")


def term_pretty_string(term: Term) -> str:
    report = term.name
    if term.type == 'constructor':
        report += '(' + ', '.join(str(t) for t in term.args) + ')'
    return report


Term.__repr__ = term_pretty_string
Term.__len__ = lambda x: len(x.args)

data = dict()


def get_unification(term1: Term, term2: Term) -> tuple:
    if term1.type == term2.type == 'const' and term1.name == term2.name:
        return None, [term1]
    elif term1.type == 'var':
        return term2, [f'{term1}:={term2}']
    elif term2.type == 'var':
        return term1, [f'{term2}:={term1}']
    elif term1.type == term2.type == 'constructor' and term1.name == term2.name:
        args = []
        subs = []
        for arg1, arg2 in zip(term1.args, term2.args):
            u_res = get_unification(arg1, arg2)
            if u_res:
                args.append(u_res[0])
                subs.extend(u_res[1])
            else:
                return
        return Term('constructor', term1.name, args), subs



def read_data(path: str) -> dict:
    return json.load(open(path, 'r'))


def parse_data(data: dict) -> dict:
    for k, v in data.items():
        data[k] = v.replace(' ', '')

    # parse constructors and constants
    constructors = {}
    constants = []
    for raw_const in data['constructors'].split(','):
        name = raw_const[0]
        var_number = int(raw_const[2:-1])
        if var_number:
            constructors[name] = var_number
        else:
            constants.append(name)

    data['constructors'] = constructors
    data['constants'] = constants

    # parse vars
    data['variables'] = data['variables'].split(',')

    # parse terms
    for key in ['first', 'second']:
        if str.count(data[key], '(') != str.count(data[key], ')'):
            data[key] = None
        else:
            term = get_term(data[key])
            if term and len(term) == data['constructors'][term.name]:
                data[key] = term
            else:
                data[key] = None

    return data


def get_term(term: str) -> Term:
    global data

    def parse_term(cur_i=0) -> Term:
        res = []
        i = cur_i
        while i < len(term):
            if term[i] in data['constructors'].keys() and term[i + 1] == '(':
                parse_res = parse_term(i + 2)
                if parse_res is None:
                    return
                res.append(parse_res[0])
                i = parse_res[1]
            elif term[i] == ')':
                t = Term('constructor', term[cur_i - 2], res)
                if len(t) == data['constructors'][t.name]:
                    return Term('constructor', term[cur_i - 2], res), i
                else:
                    return
            elif term[i] in data['constants']:
                res.append(Term('const', term[i], []))
            elif term[i] in data['variables']:
                res.append(Term('var', term[i], []))
            elif term[i] != ',':
                return
            i += 1
        return res[0]

    return parse_term()


def main() -> None:
    global data
    input_path = 'input_task_1.json'
    data = read_data(input_path)
    data = parse_data(data)
    terms = [data[k] for k in ['first', 'second']]

    if all(terms):
        unification = get_unification(*terms)
        if unification:
            print('Подстановки:')
            for sub in unification[1]:
                print(sub)
            if unification[0]:
                print(f'Унификатор: {unification[0]}')
        else:
            print('Унификация невозможна')
    else:
        print('Не соответствует грамматике')




if __name__ == '__main__':
    main()
