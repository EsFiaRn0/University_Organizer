from dataclasses import dataclass
from datetime import date
import calendar as cal


@dataclass(frozen=True)
class MonthView:
    year: int
    month: int
    month_name: str
    weeks: list[list[int]]
    today_day: int | None
    prev_year: int
    prev_month: int
    next_year: int
    next_month: int


def build_month_view(year: int, month: int) -> MonthView:
    if month < 1:
        year -= 1
        month = 12
    elif month > 12:
        year += 1
        month = 1

    c = cal.Calendar(firstweekday=0) 
    weeks = []
    week = []
    for d in c.itermonthdays(year, month):
        week.append(d)
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append(0)
        weeks.append(week)

    today = date.today()
    today_day = today.day if (today.year == year and today.month == month) else None

    # navegación
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    return MonthView(
        year=year,
        month=month,
        month_name=cal.month_name[month],
        weeks=weeks,
        today_day=today_day,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
    )