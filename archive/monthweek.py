import calendar
import datetime
from typing import NamedTuple, Dict
import pywikibot
import sys


class ProjectPage(NamedTuple):
    """프로젝트 문서 페이지 정보를 나타내는 NamedTuple."""
    name: str
    isWeek: bool  # False: 월별 문서, True: 주별 문서


# PPDICT에 대한 타입 주석: key는 str, 값은 ProjectPage
PPDICT: Dict[str, ProjectPage] = {
    '사': ProjectPage('사랑방', True),
    '기': ProjectPage('사랑방 (기술)', False),
    '질': ProjectPage('질문방', True),
    '삭토': ProjectPage('삭제 토론', False),
    '봇편': ProjectPage('봇 편집 요청', False),
    '문관': ProjectPage('문서 관리 요청', False),
    '문이': ProjectPage('이동 요청', False),
    '사관': ProjectPage('사용자 관리 요청', True)
}


def weeks_for_year(year: int) -> int:
    """
    주어진 연도(year)가 ISO 8601 기준으로 53주가 있는지 확인한 뒤,
    53주가 유효하면 53을, 그렇지 않으면 52를 반환합니다.

    Args:
        year (int): ISO 주 수를 확인할 연도 (예: 2024)

    Returns:
        int: 53주가 존재하면 53, 아니면 52
    """
    try:
        _ = datetime.date.fromisocalendar(year, 53, 7)  # 일요일(7)
        return 53
    except ValueError:
        return 52


def week_of_month(tgtdate: datetime.date) -> int:
    """
    인자로 받은 날짜가 해당 달에서 몇 번째 주에 속하는지 계산해 반환합니다.

    내부 로직상, (tgtdate.month)의 1일부터 시작해
    'd.day - d.weekday() > 0'이 되는 가장 첫 날짜를 해당 달의 '시작 주'로 간주하고,
    그 이후 (tgtdate - startdate)를 7일 단위로 나눈 값 + 1을 반환합니다.

    Args:
        tgtdate (datetime.date): 몇 번째 주인지 계산할 날짜

    Returns:
        int: 해당 날짜가 달 안에서 몇 번째 주인지
    """
    days_this_month = calendar.mdays[tgtdate.month]

    for i in range(1, days_this_month):
        d = datetime.date(tgtdate.year, tgtdate.month, i)
        if d.day - d.weekday() > 0:
            startdate = d
            break

    return (tgtdate - startdate).days // 7 + 1


def main(argv: list[str]) -> None:
    """
    메인 함수.
    인자로부터 연도와 키워드를 받아, 주별 문서나 월별 문서를 생성합니다.

    Args:
        argv (list[str]): 
            - argv[1]: 연도(예: "2025")
            - argv[2]: 키워드(예: "사" - 사랑방)

    Raises:
        ValueError: 
            - 인자 개수가 3개가 아닐 때
            - 주어진 키워드가 PPDICT에 없을 때
    """
    if len(argv) != 3:
        raise ValueError('인자가 3개여야 합니다. 예: monthweek.py 2025 사')

    if argv[2] not in PPDICT:
        raise ValueError(f'유효하지 않은 키워드입니다: {argv[2]}')

    site = pywikibot.Site()
    year = int(argv[1])
    ppagevalue = PPDICT[argv[2]]

    if not ppagevalue.isWeek:
        # 월별 문서
        for month in range(1, 13):
            page = pywikibot.Page(site, f'위키백과:{ppagevalue.name}/{year}년 {month}월')
            page.text = f'<noinclude>{{{{위키백과:{ppagevalue.name}/보존|{year}|{month}}}}}</noinclude>'
            print(f'[DEBUG] {page.title()}:\n{page.text}')
            page.save('봇: 월별 문서 생성')
    else:
        # 주별 문서
        for week in range(1, weeks_for_year(year) + 1):
            iso_sunday = datetime.date.fromisocalendar(year, week, 7) # ISO 주의 일요일
            day_value = iso_sunday.day
            month_value = iso_sunday.month

            if week_of_month(datetime.date(year, month_value, day_value)) == 0:
                c_month_value = month_value - 1 if month_value != 1 else 1
                tworow = True
            else:
                c_month_value = month_value
                tworow = False

            page = pywikibot.Page(site, f'위키백과:{ppagevalue.name}/{year}년 제{week}주')
            page.text = (
                f'<noinclude>{{{{위키백과:{ppagevalue.name}/보존'
                f'{"2" if ppagevalue.name != "사랑방" else ""}'
                f'|년={year}|월={c_month_value}|주={week}'
                f'{"|2단=예" if tworow else ""}}}}}</noinclude>'
            )
            print(f'[DEBUG] {page.title()}:\n{page.text}')
            page.save('봇: 주별 문서 생성')


if __name__ == "__main__":
    main(sys.argv)
