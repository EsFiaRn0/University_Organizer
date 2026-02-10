from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from Model.tasks import repository as TaskRepo
from Model.subjects import repository as SubRepo

bp = Blueprint("tasks", __name__, url_prefix="/tareas")


def _leer_form():
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    deadline = request.form.get("deadline", "").strip()
    estado = request.form.get("estado", "").strip()
    prioridad = request.form.get("prioridad", "").strip()
    asig_ids = request.form.getlist("asig_ids")

    errores = []
    if not nombre:
        errores.append("El nombre es obligatorio.")
    if not deadline:
        errores.append("La fecha límite es obligatoria.")
    if estado not in TaskRepo.STATUSES:
        errores.append("El estado seleccionado no es válido.")
    if prioridad not in TaskRepo.PRIORITIES:
        errores.append("La prioridad seleccionada no es válida.")

    valid_asig_ids = _valid_asig_ids(asig_ids)

    return (
        {
            "nombre": nombre,
            "descripcion": descripcion or None,
            "deadline": deadline,
            "estado": estado,
            "prioridad": prioridad,
        },
        valid_asig_ids,
        errores,
    )


def _to_task_form(data: dict) -> dict:
    return {
        "proy_nom": data.get("nombre", ""),
        "proy_des": data.get("descripcion"),
        "proy_fec": data.get("deadline", ""),
        "proy_est": data.get("estado", "pendiente"),
        "proy_pri": data.get("prioridad", "media"),
    }


def _valid_asig_ids(raw_ids: list[str]) -> list[int]:
    try:
        ids = [int(x) for x in raw_ids]
    except ValueError:
        return []

    existing = {a["asig_id"] for a in SubRepo.get_all()}
    return [asig_id for asig_id in ids if asig_id in existing]


@bp.get("/")
def list_():
    tareas = TaskRepo.get_all()
    return render_template("tasks/list.html", tareas=tareas)


@bp.get("/new")
def new_():
    asignaturas = SubRepo.get_all()
    hoy = date.today().isoformat()
    return render_template(
        "tasks/form.html",
        modo="crear",
        tarea=None,
        asignaturas=asignaturas,
        selected_asig_ids=[],
        hoy=hoy,
    )


@bp.post("/new")
def create_():
    data, asig_ids, errores = _leer_form()
    if errores:
        for e in errores:
            flash(e, "danger")
        asignaturas = SubRepo.get_all()
        return render_template(
            "tasks/form.html",
            modo="crear",
            tarea=_to_task_form(data),
            asignaturas=asignaturas,
            selected_asig_ids=asig_ids,
            hoy=data.get("deadline"),
        )

    proy_id = TaskRepo.create(data, asig_ids)
    flash("Tarea creada.", "success")
    return redirect(url_for("tasks.view_", proy_id=proy_id))


@bp.get("/<int:proy_id>")
def view_(proy_id):
    tarea = TaskRepo.get_by_id(proy_id)
    if not tarea:
        abort(404)
    asignaturas = TaskRepo.get_subjects(proy_id)
    return render_template("tasks/detail.html", tarea=tarea, asignaturas=asignaturas)


@bp.get("/<int:proy_id>/edit")
def edit_(proy_id):
    tarea = TaskRepo.get_by_id(proy_id)
    if not tarea:
        abort(404)
    asignaturas = SubRepo.get_all()
    selected_asig_ids = TaskRepo.get_subject_ids(proy_id)
    return render_template(
        "tasks/form.html",
        modo="editar",
        tarea=tarea,
        asignaturas=asignaturas,
        selected_asig_ids=selected_asig_ids,
        hoy=tarea["proy_fec"],
    )


@bp.post("/<int:proy_id>/edit")
def update_(proy_id):
    if not TaskRepo.get_by_id(proy_id):
        abort(404)

    data, asig_ids, errores = _leer_form()
    if errores:
        for e in errores:
            flash(e, "danger")
        asignaturas = SubRepo.get_all()
        return render_template(
            "tasks/form.html",
            modo="editar",
            tarea={**_to_task_form(data), "proy_id": proy_id},
            asignaturas=asignaturas,
            selected_asig_ids=asig_ids,
            hoy=data.get("deadline"),
        )

    TaskRepo.update(proy_id, data, asig_ids)
    flash("Tarea actualizada.", "success")
    return redirect(url_for("tasks.view_", proy_id=proy_id))


@bp.post("/<int:proy_id>/delete")
def delete_(proy_id):
    if not TaskRepo.get_by_id(proy_id):
        abort(404)
    TaskRepo.delete(proy_id)
    flash("Tarea eliminada.", "warning")
    return redirect(url_for("tasks.list_"))
