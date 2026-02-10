from datetime import date
from flask import Blueprint, render_template, request

from Model.calendar.service import build_month_view
from Model.tasks import repository as TaskRepo

bp = Blueprint("calendar", __name__, url_prefix="/calendario")


@bp.get("/")
def month_current():
    today = date.today()
    year = request.args.get("y", default=today.year, type=int)
    month = request.args.get("m", default=today.month, type=int)

    view = build_month_view(year, month)
    tasks = TaskRepo.get_by_month(view.year, view.month)
    tasks_by_day = {}
    for t in tasks:
        try:
            day = int(str(t["proy_fec"]).split("-")[2])
        except (IndexError, ValueError):
            continue
        tasks_by_day.setdefault(day, []).append(t)

    priority_rank = {"alta": 3, "media": 2, "baja": 1}
    for day in tasks_by_day:
        tasks_by_day[day].sort(
            key=lambda x: priority_rank.get(x["proy_pri"], 0),
            reverse=True,
        )

    return render_template("calendar/month.html", view=view, tasks_by_day=tasks_by_day)
