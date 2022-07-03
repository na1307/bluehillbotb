# TODO: Find a better way
import re
import pywikibot
from pywikibot import pagegenerators

def getRegexes(tl: str) -> list:
    if tl != 'del' and tl != 'uc': raise Exception('Nope.')

    UCTLS = [ #UCTLS means Uncategorized Templates
        "\{\{분류 {,1}필요\}\}",
        "\{\{분류 없음\}\}",
        "\{\{uncategorized\}\}",
    ]

    DELTLS = [ #DELTLS means Delete Templates
        "\{\{삭제 {,1}신청\|",
        "\{\{삭제 {,1}요청\|",
        "\{\{삭\|",
        "\{\{삭신\|",
        "\{\{ㅅ\|",
        "\{\{ㅆ\|",
        "\{\{ㅅㅅ\|",
        "\{\{del\|",
        "\{\{delete\|",
        "\{\{speedy\|",
        "\{\{speedydelete\|",
    ]

    regexes = []

    for src in {'del': DELTLS, 'uc': UCTLS}.get(tl):
        regexes.append(re.compile(src + "\n{,1}", re.IGNORECASE))

    return regexes

def main():
    gen = pagegenerators.CategorizedPageGenerator(pywikibot.Category(pywikibot.Site(), '분류:분류 필요 문서'))

    for page in gen:
        text_base = page.text

        if not any(regex.search(text_base) for regex in getRegexes('del')):
            print("\"" + page.title() + "\" is not a candidate for speedy deletion. skipping...")
            continue

        text_mod = text_base
        for regex in getRegexes('uc'):
            text_mod = regex.sub('', text_mod)

        print("Page : \"" + page.title() + "\"")
        pywikibot.showDiff(text_base, text_mod)

        page.text = text_mod

        try:
            page.save(u"봇: 삭제 신청된 문서에서 분류 필요 틀 제거")
        except pywikibot.exceptions.LockedPageError:
            print("Page is protected.")

if __name__ == "__main__":
    main()
