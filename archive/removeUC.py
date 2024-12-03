import re
from typing import Pattern
from sys import stderr
import pywikibot
from pywikibot import pagegenerators
import enum


class RegexType(enum.Enum):
    Delete = enum.auto()
    Uncategorized = enum.auto()


def getRegex(tl: RegexType) -> Pattern:
    # UCTLS stands for Uncategorized Templates
    UCTLS = "\{\{(분류( ?필요| 없음)|uncategorized)\}\}\n?"

    # DELTLS stands for Delete Templates
    DELTLS = "\{\{(삭제 ?(신|요)청|삭신?|ㅅ{1,2}|ㅆ|del(ete)?|speedy(delete)?)\|"

    return re.compile(
        {RegexType.Delete: DELTLS, RegexType.Uncategorized: UCTLS}.get(tl),
        re.IGNORECASE,
    )


def main():
    for page in pagegenerators.CategorizedPageGenerator(
        pywikibot.Category(pywikibot.Site(), "분류:분류 필요 문서")
    ):
        text_base = page.text

        if not getRegex(RegexType.Delete).search(text_base):
            continue

        text_mod = getRegex(RegexType.Uncategorized).sub("", text_base)

        print('Page : "' + page.title() + '"', file=stderr)
        pywikibot.showDiff(text_base, text_mod)

        page.text = text_mod

        try:
            page.save("봇: 삭제 신청된 문서에서 분류 필요 틀 제거")
        except pywikibot.exceptions.LockedPageError:
            print("Page is protected.", file=stderr)


if __name__ == "__main__":
    main()
