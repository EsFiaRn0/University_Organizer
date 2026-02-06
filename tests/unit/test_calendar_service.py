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
