import random


class Weed:
    def __init__(s, word: str):
        s.word = word
        s.n = len(word)
        s.indices = set([i for i in range(len(word))])

    def __len__(s):
        return s.indices.__len__()

    def remove_range(s, bounds: [int, int]):
        [upper, lower] = bounds
        s.indices -= set([x for x in range(upper, lower + 1)])

    def remove(s, index: int):
        s.indices.discard(index)

    def random_index(s) -> int:
        return random.sample(s.indices, 1)[0]

    def split_on_index_generator(s, i: int) -> [[int, int], str]:
        for lower in range(0, i + 1):  # that range +1 is fucked up man...
            for upper in reversed(range(i, s.n + 1)):
                if upper - lower > 1:
                    yield [[lower, upper], s.word[lower:upper + 1]]

    def split_from_index_generator(s, i: int) -> [int, str]:
        for upper in reversed(range(i, s.n + 1)):
            if upper - i > 1:
                yield [upper - i, s.word[i:upper + 1]]

    def split_on_index(s, i: int) -> dict:
        return {word: bounds for [bounds, word] in s.split_on_index_generator(i)}

