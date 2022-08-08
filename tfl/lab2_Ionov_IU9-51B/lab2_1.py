import re
import numpy as np
import pandas as pd
import time

REGEXPS = dict({
    'academic': 'a(b|c)*b(a|c)*c(a|b)*e',
    'neg': '[^bce][^ae]*[^ace][^be]*[^abe][^ce]*e',
    'lazy': 'a(b|c)*?b(a|c)*?c(a|b)*?e',
})

VOCAB = ['a', 'b', 'c', 'e']

NUM_OF_TESTS = 10
MIN_TEST_LEN = 1e2
MAX_TEST_LEN = 1e5
PATH_TO_TESTS = 'data/test_regexp.txt'
PATH_TO_SAVE = 'output/regexp_test.csv'


def compare(tests):
    result = dict(zip(REGEXPS.keys(), [[] for _ in range(len(REGEXPS.keys()))]))
    result['test_len'] = []
    for i, test in enumerate(tests):
        result['test_len'].append(len(test))
        cur_group = None
        for type, regexp in REGEXPS.items():
            start_time = time.time()
            match = re.search(regexp, test)
            test_time = time.time() - start_time
            if not match:
                test_time = -1
                print(f"test {i}: {test[:10]}... isn't matched with {type}")
            if not cur_group:
                cur_group = match.group()
            else:
                if match.group() != cur_group:
                    print(match.group())
                    print(cur_group)
                    print(type)
                    print(f"on test {i} lost equality")
            result[type].append(test_time * 1_000)  # in ms
    result = pd.DataFrame(result)
    return pd.DataFrame(result)


def gen_test(path):
    with open(path, 'w') as f:
        for size in np.linspace(MIN_TEST_LEN, MAX_TEST_LEN, NUM_OF_TESTS):
            size = int(size) - 1
            s = 'a'
            s += ''.join(np.random.choice(VOCAB, size))
            f.write(s + '\n')


def read_test(path):
    return open(path, 'r').read().split('\n')[:-1]


def main():
    # gen_test(PATH_TO_TESTS)
    tests = read_test(PATH_TO_TESTS)
    result = compare(tests)
    result.to_csv(PATH_TO_SAVE, index=False)
    print(result)


if __name__ == '__main__':
    main()
