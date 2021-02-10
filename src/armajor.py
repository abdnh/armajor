from typing import List, Union, Set


class ArabicMnemonicMajor:
    def __init__(self, filename: str = "words.txt"):
        self._read_words(filename)

    def _read_words(self, filename: str) -> None:
        self.word_dict = {}
        with open(filename, encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                stripped = self._strip_rest(word)
                s = self.word_dict.get(stripped, set())
                s.add(word)
                self.word_dict[stripped] = s

    _valid_chars = {
        "م",
        "د",
        "ل",
        "ن",
        "ذ",
        "ب",
        "ت",
        "ث",
        "ع",
        "غ",
        "س",
        "ش",
        "ر",
        "ز",
        "ج",
        "خ",
        "ط",
        "ظ",
        "ض",
        "ح",
        "ص",
        "ه",
        "ك",
        "ق",
        "ف",
    }

    def _strip_rest(self, s: str) -> str:
        return "".join(c for c in s if c in self._valid_chars)

    # TODO: support custom mappings
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

    def _numbers_to_consonants(self, text: str) -> List[str]:
        numstr = "".join(reversed(text))

        def get_combs(s: str):
            "Get all possible combinations of adjacent digits."
            if len(s) < 2:
                return [(*s)]
            if len(s) == 2:
                return [(s[0], s[1]), (s,)]
            ret = []
            f = s[0]
            rest = get_combs(s[1:])
            for r in rest:
                ret.append((f, *r))
                ret.append((f + r[0], *r[1:]))
            return ret

        combs = get_combs(numstr)

        # generate a list of valid mappings for each combination
        maps = {}
        for comb in combs:
            l = []
            for chunk in comb:
                if v := self.mappings.get(chunk, None):
                    l.append(v)
                else:
                    # if any "chunk" of this combination has no valid mapping, skip the combination
                    break
            if len(l) == len(comb):
                maps[comb] = l

        def get_cons_strs(l: List, i: int):
            "Return all possible consonant strings."
            if len(l) == i + 1:
                return l[i]
            r = []
            nxt = get_cons_strs(l, i + 1)
            for j in l[i]:
                for n in nxt:
                    r.append(j + n)
            return r

        # generate consonant strings from the mappings of each combination
        ret = set()
        for v in maps.values():
            ret |= set(get_cons_strs(v, 0))

        return ret

    @staticmethod
    def clean_num(num: Union[int, str]) -> str:
        num = str(num)
        num = num.strip()
        # remove decimal separators
        num = num.replace(".", "").replace(",", "")
        # remove sign
        num = num.replace("+", "").replace("-", "")

        # validate each digit separately to preserve leading zeros
        l = []
        for i in num:
            l.append(str(int(i)))
        num = "".join(l)

        return num

    def lookup(self, num: Union[int, str]) -> Set[str]:

        res = set()
        num = self.clean_num(num)
        if not num:
            return res

        cons_list = self._numbers_to_consonants(num)
        for c in cons_list:
            if l := self.word_dict.get(c):
                res.update(l)

        return res


if __name__ == "__main__":
    major = ArabicMnemonicMajor()
    r = major.lookup("101")
    print(r)
