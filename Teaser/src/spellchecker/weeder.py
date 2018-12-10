from src.spellchecker.spellchecker import *
from src.spellchecker.weed import *


class Weeder:
    def __init__(s, checker: Spellchecker):
        s.checker = checker

    def compute_valid(s, line: str) -> int:
        weed = Weed(line)
        invalid_indices = set()
        # print('\nweeding out line =', weed.word)
        while len(weed) > 0:
            index = weed.random_index()
            found = False
            for [bounds, word] in weed.split_on_index_generator(index):
                if s.checker.contains(word):
                    weed.remove_range(bounds)
                    found = True
                    # print('best intersect =', word, ' bounds =', bounds)
                    # print('remaining indices =', weed.indices)
                    break
            if not found:
                # print('invalid index =', index, 'character =', weed.word[index])
                invalid_indices.add(index)
                weed.remove(index)

        # print('final invalid indices =', invalid_indices)
        return len(weed.word) - len(invalid_indices)

    def compute_sensible(s, line: str) -> int:
        weed = Weed(line)
        best = 0
        for i in range(weed.n):
            if weed.n - i < best:
                break
            attempt = s.compute_sensible_rec(weed, i)
            if attempt > best:
                best = attempt
        return best

    def compute_sensible_rec(s, weed: Weed, i: int) -> int:
        # print('starting from', i)
        if weed.n - i < 2:
            return 1

        best = 0
        for [length, word] in weed.split_from_index_generator(i):
            # print('length =', length, 'word =', word)
            if s.checker.contains(word):
                # print('VALID length =', length, 'word =', word)
                rest = s.compute_sensible_rec(weed, i+length+1)
                if length + rest > best:
                    best = length + rest

        return best


if __name__ == '__main__':
    sc = Spellchecker()
    weeder = Weeder(sc)
    # print(weeder.compute_sensible('boterkaas'))
    print(weeder.compute_sensible('aacnlelaaaenaanrencsraticesusmorthitwvvt'))
