from Model.tasks import repository as TaskRepo


def test_get_by_date_orders_by_priority_desc(app):
    with app.app_context():
        TaskRepo.create(
            {
                "nombre": "Baja",
                "descripcion": None,
                "deadline": "2026-06-01",
                "estado": "pendiente",
                "prioridad": "baja",
            },
            [],
        )
        TaskRepo.create(
            {
                "nombre": "Media",
                "descripcion": None,
                "deadline": "2026-06-01",
                "estado": "pendiente",
                "prioridad": "media",
            },
            [],
        )
        TaskRepo.create(
            {
                "nombre": "Alta",
                "descripcion": None,
                "deadline": "2026-06-01",
                "estado": "pendiente",
                "prioridad": "alta",
            },
            [],
        )

        rows = TaskRepo.get_by_date("2026-06-01")
        priorities = [row["proy_pri"] for row in rows]
        assert priorities == ["alta", "media", "baja"]
