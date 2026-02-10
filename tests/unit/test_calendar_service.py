from Model.calendar.service import build_month_view


def test_build_month_view_prev_next():
    view = build_month_view(2026, 1)
    assert view.prev_year == 2025
    assert view.prev_month == 12
    assert view.next_year == 2026
    assert view.next_month == 2

    view = build_month_view(2026, 12)
    assert view.prev_year == 2026
    assert view.prev_month == 11
    assert view.next_year == 2027
    assert view.next_month == 1


def test_build_month_view_normalizes_out_of_range_months():
    view = build_month_view(2026, 0)
    assert view.year == 2025
    assert view.month == 12

    view = build_month_view(2026, 13)
    assert view.year == 2027
    assert view.month == 1

    view = build_month_view(2026, -2)
    assert view.year == 2025
    assert view.month == 10

    view = build_month_view(2026, 25)
    assert view.year == 2028
    assert view.month == 1
