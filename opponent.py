"""
Automatically play the cookie game (in 2 dimensions, for now). Prepare not to
win. The game works like so: There are two jars. Each has some cookies. You win
if you take the last cookie. You can take some n cookies from any combination
of jars - but n for each jar. (ie for the two-jar case, you must take either
the same from both or any number you like from one.
"""

import argparse

from operator import sub

def positive_int(s):
    v = int(s)
    if v >= 0:
        return v
    raise TypeError("should be positive integer")

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-p", "--pairs", type=int,
                        help="print pairs up to this value")

    #nargs could be "+" here, for more dimensions...
    parser.add_argument("-j", "--jars", required=True, type=positive_int, nargs=2,
                        help="jar values")
    return parser.parse_args()

def generate_pairs(n):
    state = [True] + [False] * n * 2
    pairs = [(0, 0)]
    diff = 0
    curr_n = 0
    while curr_n <= n:
        diff += 1
        curr_n = state.index(False, curr_n)
        state[curr_n] = state[curr_n + diff] = True
        pairs.append((curr_n, curr_n + diff))
    return pairs

def read_move(jars):
    ja, jb = jars
    while True:
        try:
            a, b = map(positive_int, input("Enter two jar numbers> ").split())
            if 0 not in (a, b) and a != b:
                raise ValueError("either one jar must be 0 or they must be equal")
            if 0 == a == b:
                raise ValueError("you have to make a move")
            if a > ja or b > jb:
                raise ValueError("there aren't enough cookies to take out")
        except (ValueError, IndexError) as err:
            print(err)
            continue
        except (KeyboardInterrupt, EOFError):
            print("you run away like a little baby")
        return a, b

def player_move(jars):
    mov = read_move(jars)
    return tuple(map(sub, jars, mov))

def computer_move(jars, pairs):
    a, b = sorted(jars)
    diff_trg = b - a

    if diff_trg < len(pairs) and pairs[diff_trg][0] < a:
        print("computer takes {} cookies from both jars".format(a - pairs[diff_trg][0]))
        return pairs[diff_trg]

    for pair in pairs:
        _pa, _pb = pair
        for pa, pb in [(_pa, _pb), (_pb, _pa)]:
            for sa, sb in [(a, b), (b, a)]:
                if sa == pa and pb < sb:
                    print("computer takes {} cookie{} from jar {{ {} }}".format(sb - pb, "s" * bool(sb - pb - 1), sb))
                    return pair

    raise ValueError("computer is confused - you win")

def play(jars):
    print(__doc__)
    jars = tuple(sorted(jars))
    print("jars given: {}".format(jars))
    pairs = generate_pairs(jars[-1])

    if jars in pairs:
        print("player starts")
        jars = player_move(jars)
    else:
        print("computer starts")
    
    while any(jars):
        for player in (lambda j: computer_move(j, pairs), player_move):
            print("Jars are: \n{}".format("\n".join(map("Jar {0[0]}: {0[1]}".format, enumerate(jars)))))
            jars = player(jars)

    print("computer wins")

def main():
    args = get_args()
    if args.pairs:
        print("Here are the pairs you'll never reach:\n{}".format("\n".join(map("{0[0]} {0[1]}".format, generate_pairs(args.pairs)))))
    play(args.jars)

if __name__ == "__main__":
    main()
