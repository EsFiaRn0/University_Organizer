from pathlib import Path
import pytest
from app import create_app


@pytest.fixture()
def app(tmp_path_factory):
    db_dir = tmp_path_factory.mktemp("db")
    db_path = db_dir / "test.sqlite3"

    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=True,
        DB_PATH=str(db_path),
    )

    with app.app_context():
        from BBD.db import init_db
        init_db()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
