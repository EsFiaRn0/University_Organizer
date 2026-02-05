import sqlite3
from flask import current_app

def get_conn():
    db_path = current_app.config["DB_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    schema = """
    CREATE TABLE IF NOT EXISTS ASIG (
      asig_id  INTEGER PRIMARY KEY AUTOINCREMENT,
      asig_cod TEXT NOT NULL UNIQUE,
      asig_nom TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS PROY (
      proy_id  INTEGER PRIMARY KEY AUTOINCREMENT,
      proy_nom TEXT NOT NULL,
      proy_des TEXT,
      proy_fec TEXT NOT NULL,
      proy_est TEXT NOT NULL CHECK (proy_est IN ('pendiente','en_progreso','terminado')),
      proy_pri TEXT NOT NULL CHECK (proy_pri IN ('baja','media','alta'))
    );

    CREATE TABLE IF NOT EXISTS PRAS (
      proy_id INTEGER NOT NULL,
      asig_id INTEGER NOT NULL,
      PRIMARY KEY (proy_id, asig_id),
      FOREIGN KEY (proy_id) REFERENCES PROY(proy_id) ON DELETE CASCADE,
      FOREIGN KEY (asig_id) REFERENCES ASIG(asig_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS NOTA (
      nota_id  INTEGER PRIMARY KEY AUTOINCREMENT,
      nota_nom TEXT NOT NULL,
      nota_val REAL NOT NULL CHECK (nota_val >= 0),
      asig_id  INTEGER NOT NULL,
      FOREIGN KEY (asig_id) REFERENCES ASIG(asig_id) ON DELETE CASCADE
    );
    """
    with get_conn() as conn:
        conn.executescript(schema)