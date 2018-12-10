WITH_DUPLICATES = False

PATH_RESULTS = 'resources/results.csv'

POP_SIZE = 32
GENERATIONS = 50000
FITNESS_FUNC_LIMITS = [30, 100]
ALWAYS_INCLUDE_BEST = True
INCLUDE_BEST_RANGE = (1, 22)
FRESH_GENES_RATE = 0.01
SAVE_WHEN_FITNESS_OVER = 134
ALWAYS_CROSSOVER = True
CROSSOVER_RATE = 1
ALWAYS_MUTATE = False
MUTATE_RATE_RANGE = (0.15, 0.01)

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h",
            "i", "j", "k", "l", "m", "n", "o", "p", "q",
            "r", "s", "t", "u", "v", "w", "x", "y", "z"]

ROWS = [
    [22, 216],
    [67, 67200],
    [59, 24840],
    [56, 21450],
    [77, 122892],
    [72, 95760],
    [30, 3150],
    [67, 61560]
]

# X, Y, starting from top-left
PATHS = [
    [
        [0, 0],
        [1, 0],
        [2, 0],
        [2, 1],
        [2, 2],
        [1, 2],
        [1, 1],
        [0, 1],
        [0, 2],
        [0, 3],
        [1, 3],  # may change
        [1, 4],  # may change
        [0, 4],
        [0, 5],
        [1, 5],
        [2, 5],
        [2, 6],
        [1, 6],
        [0, 6],
        [0, 7],
        [1, 7],
        [2, 7],
        [3, 7],
        [4, 7],
        [4, 6],
        [3, 6],
        [3, 5],
        [3, 4],
        [2, 4],  # insert after this
        [2, 3],
        [3, 3],
        [3, 2],
        [3, 1],
        [3, 0],
        [4, 0],
        [4, 1],
        [4, 2],
        [4, 3],
        [4, 4],
        [4, 5]
    ],
    [
        [0, 0],
        [1, 0],
        [2, 0],
        [2, 1],
        [2, 2],
        [1, 2],
        [1, 1],
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
        [0, 5],
        [1, 5],
        [2, 5],
        [2, 6],
        [1, 6],
        [0, 6],
        [0, 7],
        [1, 7],
        [2, 7],
        [3, 7],
        [4, 7],
        [4, 6],
        [3, 6],
        [3, 5],
        [3, 4],
        [2, 4],
        [1, 4],
        [1, 3],
        [2, 3],
        [3, 3],
        [3, 2],
        [3, 1],
        [3, 0],
        [4, 0],
        [4, 1],
        [4, 2],
        [4, 3],
        [4, 4],
        [4, 5]
    ]
]

if __name__ == '__main__':
    matrix = []
    for i in range(8):
        matrix.append([0 for _ in range(5)])

    for path in PATHS:
        for i, [x, y] in enumerate(path):
            matrix[y][x] = i
        print('\nPath:')
        for row in matrix:
            print(row)
    pass
