"""Camada CONTROLLER: recebe as requisições, usa o Model e escolhe a View (template)."""
from datetime import datetime, time

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .models import TIPOS, Ocorrencia, db

bp = Blueprint("ocorrencias", __name__)


def _ler_data(texto):
    """Converte 'AAAA-MM-DD' em data. Retorna None se vier vazio ou inválido."""
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


@bp.get("/")
def listar():
    """Lista as ocorrências, com filtro opcional por tipo e período."""
    filtro = {
        "tipo": request.args.get("tipo", ""),
        "de": request.args.get("de", ""),
        "ate": request.args.get("ate", ""),
    }
    data_de = _ler_data(filtro["de"])
    data_ate = _ler_data(filtro["ate"])

    consulta = Ocorrencia.query
    if filtro["tipo"] in TIPOS:
        consulta = consulta.filter(Ocorrencia.tipo == filtro["tipo"])
    if data_de:
        consulta = consulta.filter(Ocorrencia.data_ocorrencia >= datetime.combine(data_de, time.min))
    if data_ate:
        consulta = consulta.filter(Ocorrencia.data_ocorrencia <= datetime.combine(data_ate, time.max))

    aviso = None
    if data_de and data_ate and data_de > data_ate:
        aviso = "A data inicial é maior que a data final, por isso nenhuma ocorrência aparece."

    ocorrencias = consulta.order_by(Ocorrencia.data_ocorrencia.desc()).all()
    return render_template("lista.html", ocorrencias=ocorrencias, tipos=TIPOS, filtro=filtro, aviso=aviso)


@bp.route("/ocorrencias/nova", methods=["GET", "POST"])
def nova():
    """Mostra o formulário (GET) e grava uma nova ocorrência (POST)."""
    if request.method == "POST":
        dados, erros = Ocorrencia.validar(request.form)
        if erros:
            return render_template("form.html", titulo="Registrar ocorrência", tipos=TIPOS,
                                   valores=request.form, erros=erros), 400
        ocorrencia = Ocorrencia(**dados)
        db.session.add(ocorrencia)
        db.session.commit()
        flash("Ocorrência registrada com sucesso.", "sucesso")
        return redirect(url_for("ocorrencias.detalhe", id=ocorrencia.id))

    return render_template("form.html", titulo="Registrar ocorrência", tipos=TIPOS, valores={}, erros=[])


@bp.get("/ocorrencias/<int:id>")
def detalhe(id):
    """Mostra uma ocorrência. Responde 404 se ela não existir."""
    ocorrencia = db.get_or_404(Ocorrencia, id)
    return render_template("detalhe.html", ocorrencia=ocorrencia)


@bp.route("/ocorrencias/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """Mostra o formulário preenchido (GET) e grava as alterações (POST)."""
    ocorrencia = db.get_or_404(Ocorrencia, id)

    if request.method == "POST":
        dados, erros = Ocorrencia.validar(request.form)
        if erros:
            return render_template("form.html", titulo="Editar ocorrência", tipos=TIPOS,
                                   valores=request.form, erros=erros, ocorrencia=ocorrencia), 400
        for campo, valor in dados.items():
            setattr(ocorrencia, campo, valor)
        db.session.commit()
        flash("Ocorrência atualizada com sucesso.", "sucesso")
        return redirect(url_for("ocorrencias.detalhe", id=ocorrencia.id))

    return render_template("form.html", titulo="Editar ocorrência", tipos=TIPOS,
                           valores=ocorrencia.como_formulario(), erros=[], ocorrencia=ocorrencia)


@bp.post("/ocorrencias/<int:id>/excluir")
def excluir(id):
    """Exclui uma ocorrência (a confirmação é feita no navegador, em app.js)."""
    ocorrencia = db.get_or_404(Ocorrencia, id)
    db.session.delete(ocorrencia)
    db.session.commit()
    flash("Ocorrência excluída.", "sucesso")
    return redirect(url_for("ocorrencias.listar"))
