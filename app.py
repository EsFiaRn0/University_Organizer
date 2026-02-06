import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from flask import Flask, render_template
from flask_wtf import CSRFProtect
from config import DevelopmentConfig, ProductionConfig
from BBD.db import init_db
from Controller.subjects.routes import bp as subjects_bp
from Controller.calendar.routes import bp as calendar_bp

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

    @app.get("/")
    def home():
        return render_template("home.html")

    return app

app = create_app()
