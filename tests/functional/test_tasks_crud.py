from urllib.parse import urlparse


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
    path = urlparse(resp.headers["Location"]).path
    return int(path.rstrip("/").split("/")[-1])


def test_tasks_crud_flow_with_subject_links(client):
    asig_1 = _create_subject(client, "MAT101", "Algebra")
    asig_2 = _create_subject(client, "INF201", "Programacion")

    token = _get_csrf(client, "/tareas/new")
    resp = client.post(
        "/tareas/new",
        data={
            "nombre": "Proyecto final",
            "descripcion": "Entregar documento y presentacion",
            "deadline": "2026-03-20",
            "estado": "pendiente",
            "prioridad": "alta",
            "asig_ids": [str(asig_1), str(asig_2)],
            "csrf_token": token,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 302

    task_path = urlparse(resp.headers["Location"]).path
    resp = client.get(task_path)
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "Proyecto final" in html
    assert "Entregar documento y presentacion" in html
    assert "Algebra" in html
    assert "Programacion" in html

    token = _get_csrf(client, f"{task_path}/edit")
    resp = client.post(
        f"{task_path}/edit",
        data={
            "nombre": "Proyecto final actualizado",
            "descripcion": "Solo presentacion",
            "deadline": "2026-03-25",
            "estado": "en_progreso",
            "prioridad": "media",
            "asig_ids": [str(asig_2)],
            "csrf_token": token,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 302

    resp = client.get(task_path)
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "Proyecto final actualizado" in html
    assert "Solo presentacion" in html
    assert "Programacion" in html
    assert "Algebra" not in html

    token = _get_csrf(client, task_path)
    resp = client.post(
        f"{task_path}/delete",
        data={"csrf_token": token},
        follow_redirects=False,
    )
    assert resp.status_code == 302

    resp = client.get(task_path)
    assert resp.status_code == 404
