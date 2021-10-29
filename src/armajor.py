from typing import List, Union, Set, Dict, Tuple
import unicodedata


class ArabicMnemonicMajor:
    def __init__(self, filename: str = "words.txt"):
        self._read_words(filename)

    mappings = {
        "0": {"د", "م"},
        "1": {"ل", "ن", "ذ"},
        "2": {"ب", "ت", "ث"},
        "3": {"ع", "غ", "س", "ش"},
        "4": {"ر", "ز"},
        "5": {"ج", "خ"},
        "6": {"ط", "ظ", "ض"},
        "7": {"ح", "ص"},
        "8": {"ه", "ك"},
        "9": {"ق", "ف"},
    }

    inverse_mappings = {
        "م": 0,
        "د": 0,
        "ل": 1,
        "ن": 1,
        "ذ": 1,
        "ب": 2,
        "ت": 2,
        "ث": 2,
        "ع": 3,
        "غ": 3,
        "س": 3,
        "ش": 3,
        "ر": 4,
        "ز": 4,
        "ج": 5,
        "خ": 5,
        "ط": 6,
        "ظ": 6,
        "ض": 6,
        "ح": 7,
        "ص": 7,
        "ه": 8,
        "ك": 8,
        "ق": 9,
        "ف": 9,
    }

    def _strip_rest(self, s: str) -> str:
        return "".join(c for c in s if c in self.inverse_mappings.keys())

    def _read_words(self, filename: str) -> None:
        self.word_dict: Dict[str, Set] = {}
        with open(filename, encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                stripped = self._strip_rest(word)
                s = self.word_dict.get(stripped, set())
                s.add(word)
                self.word_dict[stripped] = s

    def _numbers_to_consonants(self, text: str) -> Set[str]:
        numstr = "".join(reversed(text))

        maps = []
        for letter in numstr:
            maps.append(self.mappings.get(letter))

        # TODO: speed this up
        def get_cons_strs(l: List, i: int) -> Set[str]:
            "Return all possible consonant strings."
            if len(l) == i + 1:
                return l[i]
            r = set()
            nxt = get_cons_strs(l, i + 1)
            for j in l[i]:
                for n in nxt:
                    r.add(j + n)
            return r

        return get_cons_strs(maps, 0)

    @staticmethod
    def clean_num(num: Union[int, str]) -> str:
        num = str(num)
        # strip non-digits and convert to Arabic numerals
        num = "".join(str(int(c)) for c in num if unicodedata.category(c) == "Nd")

        return num

    def lookup(self, num: Union[int, str]) -> Set[str]:

        res: Set = set()
        num = self.clean_num(num)
        if not num:
            return res

        cons_list = self._numbers_to_consonants(num)
        for c in cons_list:
            if l := self.word_dict.get(c):
                res.update(l)

        return res

    def word_to_num(self, word: str) -> str:
        word = self._strip_rest(word)
        num = []
        for c in word:
            num.append(str(self.inverse_mappings[c]))
        return "".join(reversed(num))


if __name__ == "__main__":
    major = ArabicMnemonicMajor()
    r = major.lookup("101")
    print(r)
