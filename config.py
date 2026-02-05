import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class BaseConfig:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    TEMPLATES_FOLDER = "View"
    DB_PATH = BASE_DIR / "BBD" / "organizador.db"
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
