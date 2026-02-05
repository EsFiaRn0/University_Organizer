from BBD.db import get_conn

def get_all():
    with get_conn() as conn:
        return conn.execute("""
            SELECT asig_id, asig_cod, asig_nom
            FROM ASIG
            ORDER BY asig_cod ASC
        """).fetchall()

def get_by_id(asig_id: int):
    with get_conn() as conn:
        return conn.execute("""
            SELECT asig_id, asig_cod, asig_nom
            FROM ASIG
            WHERE asig_id = ?
        """, (asig_id,)).fetchone()

def create(data: dict):
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO ASIG (asig_cod, asig_nom)
            VALUES (?, ?)
        """, (data["codigo"], data["nombre"]))
        return cur.lastrowid

def update(asig_id: int, data: dict):
    with get_conn() as conn:
        conn.execute("""
            UPDATE ASIG
            SET asig_cod = ?, asig_nom = ?
            WHERE asig_id = ?
        """, (data["codigo"], data["nombre"], asig_id))

def delete(asig_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM ASIG WHERE asig_id = ?", (asig_id,))
