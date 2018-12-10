class Spellchecker:

    def __init__(s):
        with open('/usr/share/dict/nederlands', encoding='utf-8') as data_file:
            s.nl = set(data_file.read().splitlines())

    def intersect(s, word: [str]) -> [str]:
        return [x for x in word if x in s.nl]

    def intersect_amount(s, word: [str]) -> int:
        return len(s.intersect(word))

    def contains(s, word: str) -> bool:
        return word in s.nl


if __name__ == '__main__':
    sc = Spellchecker()
    print(len(sc.nl))
