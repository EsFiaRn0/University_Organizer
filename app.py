import os
from datetime import date, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from flask import Flask, render_template
from flask_wtf import CSRFProtect
from config import DevelopmentConfig, ProductionConfig
from BBD.db import init_db
from Controller.subjects.routes import bp as subjects_bp
from Controller.calendar.routes import bp as calendar_bp
from Controller.tasks.routes import bp as tasks_bp
from Model.subjects import repository as SubRepo
from Model.calendar.service import build_month_view
from Model.tasks import repository as TaskRepo

def create_app():
    app = Flask(__name__, template_folder="View")

    env = os.getenv("APP_ENV", os.getenv("FLASK_ENV", "development")).lower()
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("FLASK_SECRET_KEY no definida en .env")

    with app.app_context():
        init_db()

    CSRFProtect(app)

    app.register_blueprint(subjects_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(tasks_bp)

    @app.get("/")
    def home():
        subjects = SubRepo.get_all()
        total_asignaturas = len(subjects)
        view = build_month_view(date.today().year, date.today().month)
        today = date.today()
        today_str = today.isoformat()
        tareas_hoy = TaskRepo.get_by_date(today_str)
        end_date = (today + timedelta(days=4)).isoformat()
        tareas_rango = TaskRepo.get_between(today_str, end_date)
        total_tareas_rango = len(tareas_rango)

        month_tasks = TaskRepo.get_by_month(view.year, view.month)
        day_priorities = {}
        for t in month_tasks:
            try:
                day = int(str(t["proy_fec"]).split("-")[2])
            except (IndexError, ValueError):
                continue
            day_priorities.setdefault(day, set()).add(t["proy_pri"])

        return render_template(
            "home.html",
            asignaturas=subjects,
            view=view,
            tareas_hoy=tareas_hoy,
            tareas_rango=tareas_rango,
            day_priorities=day_priorities,
            today_str=today_str,
            total_asignaturas=total_asignaturas,
            total_tareas_rango=total_tareas_rango,
        )

    return app

app = create_app()
