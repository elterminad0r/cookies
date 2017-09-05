import sys
import argparse
import itertools

from collections import deque

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jars", type=int, default=2, help="number of jars")
    parser.add_argument("-m", "--maxc", type=int, default=10, help="maximum number of cookies")
    parser.add_argument("-s", "--solve", type=int, nargs="+", help="try to solve this state")
    parser.add_argument("-p", "--print-safes", action="store_true", help="print found safe states")
    parser.add_argument("-i", "--interactive", action="store_true", help="interactively keep solving")
    parser.add_argument("-n", "--normalise", action="store_true", help="normalise from smallest")
    return parser.parse_args()

def _lex_jars(choices, jars, acc=deque()):
    if jars == 1:
        yield list(acc) + [choices[-1]]
    elif jars:
        for ind, i in enumerate(choices):
            acc.append(i)
            yield from _lex_jars(choices[ind:], jars - 1, acc)
            acc.pop()

def gen_states(jars, max_cookies):
    for i in range(1, max_cookies + 1):
        yield from _lex_jars(range(i), jars)

def index_combinations(jars):
    return itertools.chain.from_iterable(itertools.combinations(range(jars), r) for r in range(1, jars+1))

def generate_moves(jars, max_move):
    for indices in index_combinations(jars):
        l = [0 for _ in range(jars)]
        for i in range(1, max_move + 1):
            for ind in indices:
                l[ind] = i
            yield l

def branch(state, max_move):
    jars = len(state)
    for i in generate_moves(jars, max_move):
        yield tuple(sorted(a + b for a, b in zip(state, i)))

def find_safe_states(jars, max_cookies):
    safe_states = []
    unsafe_states = set()
    for _i in gen_states(jars, max_cookies):
        i = sorted(_i)
        if tuple(i) not in unsafe_states:
            brn = set(branch(i, max_cookies))
            safe_states.append((i, brn))
            unsafe_states.update(brn)
    return safe_states, unsafe_states

def check_safes(safes, max_cookies):
    unsafes = set()
    for i in safes:
        unsafes.update(i[1])
    assert not any(tuple(i[0]) in unsafes for i in safes)
    print("safe states appear safe")

def pp_safes(jars, maxc, safes):
    topl = len(str(maxc)) + 1
    for i in safes:
        print(("{{:>{}d}}".format(topl) * jars).format(*i[0]))

def find_safe_jump(jars, maxc, state, gsafes):
    if state:
        assert max(state) < maxc
        assert min(state) >= 0
        assert len(state) == jars
        state = tuple(sorted(state))
        safes, branches = zip(*gsafes)
        if list(state) in safes:
            print("this *is* a safe state")
        else:
            for ind, i in enumerate(branches):
                if state in i:
                    print("{} can be reduced to {}".format(state, safes[ind]))
                    for j in generate_moves(jars, maxc):
                        if tuple(sorted(a + b for a, b in zip(safes[ind], j))) == state:
                            print("using move {} on\n".format(j) +
                                  "           {}".format(safes[ind]))
                            break
                    break
            else:
                print("this looks pretty bad i can't see a way out")

def read_state():
    inp = input("enter a state> ")
    try:
        return [int(i) for i in inp.split()]
    except ValueError:
        print("invalid input")
        return read_state()

def main():
    args = get_args()
    safes, u = find_safe_states(args.jars, args.maxc)
    print("calculated")

    check_safes(safes, args.maxc)
    safes.sort()

    if args.print_safes:
        pp_safes(args.jars, args.maxc, safes)

    find_safe_jump(args.jars, args.maxc, args.solve, safes)

    if args.normalise:
        pp_safes(args.jars, args.maxc, [([i - s[0][0] for i in s[0]], None) for s in safes])

    if args.interactive:
        try:
            while True:
                try:
                    find_safe_jump(args.jars, args.maxc, read_state(), safes)
                except AssertionError:
                    print("invalid input")
        except (KeyboardInterrupt, EOFError):
            print("bye :)")

if __name__ == "__main__":
    main()
