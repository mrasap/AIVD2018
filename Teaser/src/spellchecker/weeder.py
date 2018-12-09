from src.spellchecker.spellchecker import *
from src.spellchecker.weed import *


class Weeder:
    def __init__(s, checker: Spellchecker):
        s.checker = checker

    def weed_out(s, line: str) -> int:
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


if __name__ == '__main__':
    sc = Spellchecker()
    weeder = Weeder(sc)
    print(weeder.weed_out('aacnlelaaaenaanrencsraticesusmorthitwvvt'))
