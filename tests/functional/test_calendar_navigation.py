from datetime import date


def test_calendar_navigation_links(client):
    today = date.today()
    resp = client.get(f"/calendario/?y={today.year}&m={today.month}")
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")

    prev_month = today.month - 1
    prev_year = today.year
    if prev_month < 1:
        prev_month = 12
        prev_year -= 1

    next_month = today.month + 1
    next_year = today.year
    if next_month > 12:
        next_month = 1
        next_year += 1

    assert f"/calendario/?y={prev_year}&amp;m={prev_month}" in html
    assert f"/calendario/?y={next_year}&amp;m={next_month}" in html
