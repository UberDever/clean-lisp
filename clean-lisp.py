import re
from dataclasses import dataclass
import itertools
from pprint import pprint


def flatmap(func, *iterable):
    return itertools.chain.from_iterable(map(func, *iterable))


tests = [
    (
        """
        Def Fact n
            If == n 0
               1
               * n Fact - n 1

        Def Main
            + Fact 5; 1
        """,
        """
        (def (fact n)
            (if (== n 0) 1 (* n (fact (- n 1)))))
        (def (main) (+ (fact 5) 1))
        """
    ),
]


@dataclass
class TokenStr:
    s: str


@dataclass
class TokenSpace:
    count: int


@dataclass
class TokenDelim:
    delim: str


Token = TokenStr | TokenSpace | TokenDelim


class Lexer:

    special = ['.', ';']

    def reduce_spaces(self, s: list[str]) -> list[Token]:
        non_empty = [t for t in s if len(t) > 0]

        def separate_tokens(t: str) -> list[str]:
            if any(t.startswith(cuttable) for cuttable in self.special):
                return [t[0], t[1:]]
            elif any(t.endswith(cuttable) for cuttable in self.special):
                return [t[-1], t[0:-1]]
            else:
                return [t]

        def to_token(t: str) -> Token:
            if t == '\n' or t in self.special:
                return TokenDelim(t)
            elif t.isspace():
                count = t.count(' ')
                return TokenSpace(count)
            else:
                return TokenStr(t)

        separate = flatmap(separate_tokens, non_empty)
        tokens = map(to_token, separate)

        return list(tokens)

    def do(self, s: str) -> str:
        split_tokens = [t for t in re.split(r'(\n|[ \t\x0B\f\r]+)', s) if t]
        reduced_tokens = self.reduce_spaces(split_tokens)
        pprint(reduced_tokens)
        return ""


l = Lexer()
for code, expected in tests:
    tokens = l.do(code)
    # print(tokens)
