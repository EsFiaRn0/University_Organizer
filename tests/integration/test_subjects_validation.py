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


def test_subjects_empty_fields(client):
    token = _get_csrf(client, "/asignaturas/new")
    resp = client.post(
        "/asignaturas/new",
        data={"codigo": "", "nombre": "", "csrf_token": token},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "El código es obligatorio." in html
    assert "El nombre es obligatorio." in html


def test_subjects_duplicate_code(client):
    token = _get_csrf(client, "/asignaturas/new")
    resp = client.post(
        "/asignaturas/new",
        data={"codigo": "INF100", "nombre": "Intro", "csrf_token": token},
        follow_redirects=False,
    )
    assert resp.status_code == 302

    token = _get_csrf(client, "/asignaturas/new")
    resp = client.post(
        "/asignaturas/new",
        data={"codigo": "INF100", "nombre": "Intro 2", "csrf_token": token},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "Ese código ya existe. Usa otro." in html
