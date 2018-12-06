alphabet = ["a", "b", "c", "d", "e", "f", "g", "h",
            "i", "j", "k", "l", "m", "n", "o", "p", "q",
            "r", "s", "t", "u", "v", "w", "x", "y", "z"]

rows = [
    [22, 216],
    [67, 67200],
    [59, 24840],
    [56, 21450],
    [77, 122892],
    [72, 95760],
    [30, 3150],
    [67, 61560]
]

path = [
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
    [1, 3],
    [1, 4],
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


def modulo(product: int) -> [int]:
    lettersIndex = []
    for i in range(1, 27):
        if (product % i == 0):
            lettersIndex.append(i)
    return lettersIndex


def rowToLetters(letters: [int]) -> [str]:
    let = []
    for i in letters:
        let.append(alphabet[i - 1])
    return let


def matrixToLetters(matrix: [[int]]) -> [[str]]:
    let = []
    for row in matrix:
        let.append(rowToLetters(row))
    return let


def bruteForceLetters(letters: [int], withDuplicates: bool = True) -> [int]:
    nm = len(letters)
    if (withDuplicates):
        for a in range(nm):
            for b in range(nm):
                for c in range(nm):
                    for d in range(nm):
                        for e in range(nm):
                            yield [letters[a],
                                   letters[b],
                                   letters[c],
                                   letters[d],
                                   letters[e]]
    else:
        for a in range(nm):
            for b in range(a, nm):
                for c in range(b, nm):
                    for d in range(c, nm):
                        for e in range(d, nm):
                            yield [letters[a],
                                   letters[b],
                                   letters[c],
                                   letters[d],
                                   letters[e]]


def sumOfRow(letters: [int]) -> int:
    s = 0
    for i in letters:
        s += i
    return s


def productOfRow(letters: [int]) -> int:
    s = 1
    for i in letters:
        s *= i
    return s


def bruteForceRows(matrix: [[int]]) -> [[int]]:
    for a in range(len(matrix[0])):
        for b in range(len(matrix[1])):
            for c in range(len(matrix[2])):
                for d in range(len(matrix[3])):
                    for e in range(len(matrix[4])):
                        for f in range(len(matrix[5])):
                            for g in range(len(matrix[6])):
                                for h in range(len(matrix[7])):
                                    yield [matrix[0][a],
                                           matrix[1][b],
                                           matrix[2][c],
                                           matrix[3][d],
                                           matrix[4][e],
                                           matrix[5][f],
                                           matrix[6][g],
                                           matrix[7][h]]


def matrixToString(matrix: [[int]], path: [[int]]) -> str:
    ret: str = ""

    for [x, y] in path:
        ret += alphabet[matrix[y][x] - 1]

    return ret


if __name__ == '__main__':
    # PARAMS
    # If you want to have all possible permutations of a row, or not
    WITH_DUPLICATES = False

    # Simply checking whether the path is correct
    xs = [0 for _ in range(5)]
    ys = [0 for _ in range(8)]
    for [x, y] in path:
        xs[x] += 1
        ys[y] += 1
    print(xs)
    print(ys)

    # First, I bruteforce all the possible rows of letters, and store them in a matrix.
    # This matrix consists of a list of 8 rows, and each row consists of a list of all possible
    # combinations of letters.
    combinationOfLettersPerRow = []
    i = 0
    for row in rows:
        print("\nNew row:", row)
        r = []
        letters = modulo(row[1])
        for combination in bruteForceLetters(letters=letters, withDuplicates=WITH_DUPLICATES):
            if sumOfRow(combination) == row[0] and productOfRow(combination) == row[1]:
                # print(rowToLetters(combination))
                r.append(combination)
                i += 1
        combinationOfLettersPerRow.append(r)

    print(i)

    # Then, I bruteforce all the possible combinations between the rows
    # This outputs a 2D matrix, where all numbers refer to the index of the alphabet
    # I turn this 2D matrix into a string, based on the path
    # A second path is possible that I didn't include yet
    j = 0
    for combination in bruteForceRows(combinationOfLettersPerRow):
        j += 1
        print(matrixToString(combination, path))

    print(j)
