from src.config import *
import csv


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


def bruteForceRows(matrix: [[str]]) -> [[str]]:
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


def intMatrixToString(matrix: [[int]], path: [[int]]) -> str:
    ret: str = ""
    for [x, y] in path:
        ret += alphabet[matrix[y][x] - 1]
    return ret


def strMatrixToString(matrix: [[str]], path: [[int]]) -> str:
    ret: str = ""
    for [x, y] in path:
        ret += matrix[y][x]
    return ret


def writeResultsToCsv(matrix: [[str, int]]):
    with open(PATH_RESULTS, 'a') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)
