from urllib.parse import urlparse

from Model.tasks import repository as TaskRepo


def _get_csrf(client, path):
    resp = client.get(path)
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    marker = 'name="csrf_token" value="'
    start = html.find(marker)
    assert start != -1
    start += len(marker)
    end = html.find('"', start)
    assert end != -1
    return html[start:end]


def _create_subject(client, code, name):
    token = _get_csrf(client, "/asignaturas/new")
    resp = client.post(
        "/asignaturas/new",
        data={"codigo": code, "nombre": name, "csrf_token": token},
        follow_redirects=False,
    )
    assert resp.status_code == 302
    return int(urlparse(resp.headers["Location"]).path.rstrip("/").split("/")[-1])


def test_tasks_empty_required_fields(client, app):
    token = _get_csrf(client, "/tareas/new")
    resp = client.post(
        "/tareas/new",
        data={
            "nombre": "",
            "descripcion": "x",
            "deadline": "",
            "estado": "pendiente",
            "prioridad": "media",
            "csrf_token": token,
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "El nombre es obligatorio." in html
    assert "obligatoria." in html

    with app.app_context():
        assert TaskRepo.get_all() == []


def test_tasks_invalid_status_and_priority(client, app):
    token = _get_csrf(client, "/tareas/new")
    resp = client.post(
        "/tareas/new",
        data={
            "nombre": "Tarea invalida",
            "descripcion": "",
            "deadline": "2026-04-01",
            "estado": "otro",
            "prioridad": "urgente",
            "csrf_token": token,
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "estado seleccionado" in html
    assert "prioridad seleccionada" in html

    with app.app_context():
        assert TaskRepo.get_all() == []


def test_tasks_non_existing_subject_ids_are_ignored(client):
    _create_subject(client, "HIS101", "Historia")

    token = _get_csrf(client, "/tareas/new")
    resp = client.post(
        "/tareas/new",
        data={
            "nombre": "Leer capitulo",
            "descripcion": "",
            "deadline": "2026-05-02",
            "estado": "pendiente",
            "prioridad": "baja",
            "asig_ids": ["99999"],
            "csrf_token": token,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 302
    task_path = urlparse(resp.headers["Location"]).path

    resp = client.get(task_path)
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "No hay asignaturas asociadas." in html
