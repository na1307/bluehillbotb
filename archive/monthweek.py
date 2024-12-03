import calendar
import datetime
import math
from collections import namedtuple
import pywikibot
import sys


ProjectPage = namedtuple('ProjectPage', ['name', 'isWeek'])


# False: 월별 문서
# True: 주별 문서
PPDICT = {
    '사': ProjectPage('사랑방', True),
    '기': ProjectPage('사랑방 (기술)', False),
    '질': ProjectPage('질문방', True),
    '삭토': ProjectPage('삭제 토론', False),
    '봇편': ProjectPage('봇 편집 요청', False),
    '문관': ProjectPage('문서 관리 요청', False),
    '문이': ProjectPage('이동 요청', False),
    '사관': ProjectPage('사용자 관리 요청', True)
}


def weeks_for_year(year):
    last_week = datetime.date(year, 12, 28)
    return last_week.isocalendar().week


def week_of_month(tgtdate):
    days_this_month = calendar.mdays[tgtdate.month]

    for i in range(1, days_this_month):
        d = datetime.date(tgtdate.year, tgtdate.month, i)
        if d.day - d.weekday() > 0:
            startdate = d
            break

    return (tgtdate - startdate).days //7 + 1


def main(argv: list[str]):
    if len(argv) != 3:
        raise Exception('asdf1')

    if argv[2] not in PPDICT:
        raise Exception('asdf2')

    site = pywikibot.Site()
    year = argv[1]
    ppagevalue = PPDICT.get(argv[2])

    if not ppagevalue.isWeek:
        for month in range(1, 13):
            c_text = '<noinclude>{{위키백과:' + ppagevalue.name + '/보존|' + year + '|' + str(month) +'}}</noinclude>'
            page = pywikibot.Page(site, '위키백과:' + ppagevalue.name + '/' + year + '년 ' + str(month) + '월')
            page.text = c_text
            print(page.text)
            page.save('봇: 월별 문서 생성')
    else:
        wfy = weeks_for_year(int(year))

        for week in range(1, wfy + 1):
            month_value = math.ceil(week / (wfy / 12))

            if week_of_month(datetime.date(int(year), month_value, datetime.datetime.strptime(year + '-W' + str(week) + '-0', "%Y-W%W-%w").day)) == 0:
                c_month_value = month_value - 1
                tworow = True
            else:
                c_month_value = month_value
                tworow = False

            c_text = '<noinclude>{{위키백과:' + ppagevalue.name + '/보존' + ('2' if ppagevalue.name != '사랑방' else '') + '|년=' + year + '|월=' + str(c_month_value)  + '|주=' + str(week) + ('|2단=예' if tworow else '') +'}}</noinclude>'
            page = pywikibot.Page(site, '위키백과:' + ppagevalue.name + '/' + year + '년 제' + str(week) + '주')
            page.text = c_text
            print(page.text)
            page.save('봇: 주별 문서 생성')


if __name__ == "__main__":
    main(sys.argv)
