from BBD.db import get_conn
import calendar as cal

STATUSES = ("pendiente", "en_progreso", "terminado")
PRIORITIES = ("baja", "media", "alta")


def get_all():
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT proy_id, proy_nom, proy_des, proy_fec, proy_est, proy_pri
            FROM PROY
            ORDER BY proy_fec ASC, proy_id DESC
            """
        ).fetchall()


def get_by_date(date_str: str):
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT proy_id, proy_nom, proy_des, proy_fec, proy_est, proy_pri
            FROM PROY
            WHERE proy_fec = ?
            ORDER BY proy_pri DESC, proy_id DESC
            """,
            (date_str,),
        ).fetchall()


def get_by_month(year: int, month: int):
    last_day = cal.monthrange(year, month)[1]
    start = f"{year:04d}-{month:02d}-01"
    end = f"{year:04d}-{month:02d}-{last_day:02d}"
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT proy_id, proy_nom, proy_des, proy_fec, proy_est, proy_pri
            FROM PROY
            WHERE proy_fec BETWEEN ? AND ?
            ORDER BY proy_fec ASC, proy_pri DESC, proy_id DESC
            """,
            (start, end),
        ).fetchall()


def get_between(start_date: str, end_date: str):
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT proy_id, proy_nom, proy_des, proy_fec, proy_est, proy_pri
            FROM PROY
            WHERE proy_fec BETWEEN ? AND ?
            ORDER BY
              CASE proy_pri
                WHEN 'alta' THEN 3
                WHEN 'media' THEN 2
                WHEN 'baja' THEN 1
                ELSE 0
              END DESC,
              proy_fec ASC,
              proy_id DESC
            """,
            (start_date, end_date),
        ).fetchall()


def get_by_id(proy_id: int):
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT proy_id, proy_nom, proy_des, proy_fec, proy_est, proy_pri
            FROM PROY
            WHERE proy_id = ?
            """,
            (proy_id,),
        ).fetchone()


def get_subject_ids(proy_id: int) -> list[int]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT asig_id
            FROM PRAS
            WHERE proy_id = ?
            ORDER BY asig_id ASC
            """,
            (proy_id,),
        ).fetchall()
        return [r["asig_id"] for r in rows]


def get_subjects(proy_id: int):
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT a.asig_id, a.asig_cod, a.asig_nom
            FROM ASIG a
            INNER JOIN PRAS p ON p.asig_id = a.asig_id
            WHERE p.proy_id = ?
            ORDER BY a.asig_cod ASC
            """,
            (proy_id,),
        ).fetchall()


def create(data: dict, asig_ids: list[int]):
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO PROY (proy_nom, proy_des, proy_fec, proy_est, proy_pri)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["nombre"],
                data.get("descripcion"),
                data["deadline"],
                data["estado"],
                data["prioridad"],
            ),
        )
        proy_id = cur.lastrowid
        _set_subjects(conn, proy_id, asig_ids)
        return proy_id


def update(proy_id: int, data: dict, asig_ids: list[int]):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE PROY
            SET proy_nom = ?, proy_des = ?, proy_fec = ?, proy_est = ?, proy_pri = ?
            WHERE proy_id = ?
            """,
            (
                data["nombre"],
                data.get("descripcion"),
                data["deadline"],
                data["estado"],
                data["prioridad"],
                proy_id,
            ),
        )
        _set_subjects(conn, proy_id, asig_ids)


def delete(proy_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM PROY WHERE proy_id = ?", (proy_id,))


def _set_subjects(conn, proy_id: int, asig_ids: list[int]):
    conn.execute("DELETE FROM PRAS WHERE proy_id = ?", (proy_id,))
    if not asig_ids:
        return
    conn.executemany(
        "INSERT INTO PRAS (proy_id, asig_id) VALUES (?, ?)",
        [(proy_id, asig_id) for asig_id in asig_ids],
    )
