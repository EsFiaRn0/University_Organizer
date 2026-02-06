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


def test_subjects_crud_flow(client):
    token = _get_csrf(client, "/asignaturas/new")
    resp = client.post(
        "/asignaturas/new",
        data={"codigo": "MAT101", "nombre": "Álgebra", "csrf_token": token},
        follow_redirects=False,
    )
    assert resp.status_code == 302

    location = resp.headers["Location"]
    path = urlparse(location).path
    resp = client.get(path)
    assert resp.status_code == 200
    assert "Álgebra" in resp.data.decode("utf-8")

    token = _get_csrf(client, f"{path}/edit")
    resp = client.post(
        f"{path}/edit",
        data={"codigo": "MAT101", "nombre": "Álgebra II", "csrf_token": token},
        follow_redirects=False,
    )
    assert resp.status_code == 302

    resp = client.get(path)
    assert "Álgebra II" in resp.data.decode("utf-8")

    token = _get_csrf(client, path)
    resp = client.post(
        f"{path}/delete",
        data={"csrf_token": token},
        follow_redirects=False,
    )
    assert resp.status_code == 302

    resp = client.get(path)
    assert resp.status_code == 404
