from src.util.util import *
from src.spellchecker.spellchecker import Spellchecker
from src.spellchecker.weeder import Weeder

if __name__ == '__main__':
    weeder = Weeder(Spellchecker())

    # First, I bruteforce all the possible rows of letters, and store them in a matrix.
    # This matrix consists of a list of 8 rows, and each row consists of a list of all possible
    # combinations of letters.
    combinationOfLettersPerRow = []
    for row in ROWS:
        print("\nNew row:", row)
        r = []
        letters = modulo(row[1])
        for combination in bruteForceLetters(letters=letters, withDuplicates=WITH_DUPLICATES):
            if sumOfRow(combination) == row[0] and productOfRow(combination) == row[1]:
                # print(rowToLetters(combination))
                r.append(rowToLetters(combination))
        combinationOfLettersPerRow.append(r)

    # Then, I bruteforce all the possible combinations between the rows
    # This outputs a 2D matrix, where all numbers refer to the index of the alphabet
    # I turn this 2D matrix into a string, based on the path
    # A second path is possible that I didn't include yet
    resultMatrix = []
    try:
        for i, combination in enumerate(bruteForceRows(combinationOfLettersPerRow)):
            if i % 250 == 0:
                print('currently at =', i)
            line = strMatrixToString(combination, PATH)
            result = weeder.compute_valid(line)
            if result > 35:
                print(line, result)
                resultMatrix.append([line, result])

                if len(resultMatrix) > 10:
                    writeResultsToCsv(resultMatrix)
                    resultMatrix = []
    finally:
        print('Writing last results to csv')
        if len(resultMatrix) > 0:
            writeResultsToCsv(resultMatrix)
