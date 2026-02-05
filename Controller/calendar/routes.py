from datetime import date
from flask import Blueprint, render_template, request

from Model.calendar.service import build_month_view

bp = Blueprint("calendar", __name__, url_prefix="/calendario")


@bp.get("/")
def month_current():
    today = date.today()
    year = request.args.get("y", default=today.year, type=int)
    month = request.args.get("m", default=today.month, type=int)

    view = build_month_view(year, month)
    return render_template("calendar/month.html", view=view)
