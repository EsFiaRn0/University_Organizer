import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from Model.subjects import repository as SubRepo

bp = Blueprint("subjects", __name__, url_prefix="/asignaturas")

def _leer_form():
    codigo = request.form.get("codigo", "").strip()
    nombre = request.form.get("nombre", "").strip()

    errores = []
    if not codigo:
        errores.append("El código es obligatorio.")
    if not nombre:
        errores.append("El nombre es obligatorio.")
    return {"codigo": codigo, "nombre": nombre}, errores

@bp.get("/")
def list_():
    asignaturas = SubRepo.get_all()
    return render_template("subjects/list.html", asignaturas=asignaturas)

@bp.get("/new")
def new_():
    return render_template("subjects/form.html", modo="crear", asig=None)

@bp.post("/new")
def create_():
    data, errores = _leer_form()
    if errores:
        for e in errores: flash(e, "danger")
        return render_template("subjects/form.html", modo="crear", asig=data)

    try:
        asig_id = SubRepo.create(data)
    except sqlite3.IntegrityError:
        flash("Ese código ya existe. Usa otro.", "danger")
        return render_template("subjects/form.html", modo="crear", asig=data)

    flash("Asignatura creada.", "success")
    return redirect(url_for("subjects.view_", asig_id=asig_id))

@bp.get("/<int:asig_id>")
def view_(asig_id):
    asig = SubRepo.get_by_id(asig_id)
    if not asig:
        abort(404)
    return render_template("subjects/detail.html", asig=asig)

@bp.get("/<int:asig_id>/edit")
def edit_(asig_id):
    asig = SubRepo.get_by_id(asig_id)
    if not asig:
        abort(404)
    return render_template("subjects/form.html", modo="editar", asig=asig)

@bp.post("/<int:asig_id>/edit")
def update_(asig_id):
    if not SubRepo.get_by_id(asig_id):
        abort(404)

    data, errores = _leer_form()
    if errores:
        for e in errores: flash(e, "danger")
        data["asig_id"] = asig_id
        return render_template("subjects/form.html", modo="editar", asig=data)

    try:
        SubRepo.update(asig_id, data)
    except sqlite3.IntegrityError:
        flash("Ese código ya existe. Usa otro.", "danger")
        data["asig_id"] = asig_id
        return render_template("subjects/form.html", modo="editar", asig=data)

    flash("Asignatura actualizada.", "success")
    return redirect(url_for("subjects.view_", asig_id=asig_id))

@bp.post("/<int:asig_id>/delete")
def delete_(asig_id):
    if not SubRepo.get_by_id(asig_id):
        abort(404)
    SubRepo.delete(asig_id)
    flash("Asignatura eliminada.", "warning")
    return redirect(url_for("subjects.list_"))
