"""Camada CONTROLLER: recebe as requisições, usa o Model e escolhe a View (template)."""
from datetime import datetime, time

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from .models import TIPOS, Ocorrencia, db, limites_da_data

bp = Blueprint("ocorrencias", __name__)


def _ler_data(texto):
    """Converte 'AAAA-MM-DD' em data. Retorna None se vier vazio ou inválido."""
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _render_formulario(titulo, valores, erros=None, ocorrencia=None, status=200):
    return render_template("form.html", titulo=titulo, tipos=TIPOS, valores=valores,
                           erros=erros or [], ocorrencia=ocorrencia, limites=limites_da_data()), status


@bp.get("/")
def listar():
    """Lista as ocorrências (as registradas mais recentemente primeiro), com filtro e busca."""
    filtro = {
        "tipo": request.args.get("tipo", ""),
        "de": request.args.get("de", ""),
        "ate": request.args.get("ate", ""),
        "q": request.args.get("q", "").strip(),
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
    if filtro["q"]:
        termo = f"%{filtro['q']}%"
        consulta = consulta.filter(or_(Ocorrencia.local.ilike(termo), Ocorrencia.descricao.ilike(termo)))

    aviso = None
    if data_de and data_ate and data_de > data_ate:
        aviso = "A data inicial é maior que a data final, por isso nenhuma ocorrência aparece."

    filtro_ativo = any(filtro.values())
    ocorrencias = consulta.order_by(Ocorrencia.criado_em.desc()).all()
    return render_template("lista.html", ocorrencias=ocorrencias, tipos=TIPOS, filtro=filtro,
                           filtro_ativo=filtro_ativo, aviso=aviso)


@bp.route("/ocorrencias/nova", methods=["GET", "POST"])
def nova():
    """Mostra o formulário (GET) e grava uma nova ocorrência (POST)."""
    if request.method == "POST":
        dados, erros = Ocorrencia.validar(request.form)
        if erros:
            return _render_formulario("Registrar ocorrência", request.form, erros, status=400)
        ocorrencia = Ocorrencia(**dados)
        db.session.add(ocorrencia)
        db.session.commit()
        flash("Ocorrência registrada com sucesso.", "sucesso")
        return redirect(url_for("ocorrencias.detalhe", id=ocorrencia.id))

    # A data e a hora já vêm preenchidas com o momento atual: na maioria das vezes
    # o morador registra logo depois do que aconteceu.
    agora = {"data_ocorrencia": datetime.now().strftime("%Y-%m-%dT%H:%M")}
    return _render_formulario("Registrar ocorrência", agora)


@bp.get("/ocorrencias/<int:id>")
def detalhe(id):
    """Mostra uma ocorrência. Responde 404 se ela não existir."""
    ocorrencia = db.get_or_404(Ocorrencia, id)
    link = url_for("ocorrencias.detalhe", id=ocorrencia.id, _external=True)
    texto_whatsapp = (f"Alerta Vizinhos: {ocorrencia.tipo} em {ocorrencia.local}, "
                      f"{ocorrencia.data_ocorrencia.strftime('%d/%m/%Y %H:%M')}. Detalhes: {link}")
    return render_template("detalhe.html", ocorrencia=ocorrencia, texto_whatsapp=texto_whatsapp)


@bp.route("/ocorrencias/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """Mostra o formulário preenchido (GET) e grava as alterações (POST)."""
    ocorrencia = db.get_or_404(Ocorrencia, id)

    if request.method == "POST":
        dados, erros = Ocorrencia.validar(request.form)
        if erros:
            return _render_formulario("Editar ocorrência", request.form, erros, ocorrencia, status=400)
        for campo, valor in dados.items():
            setattr(ocorrencia, campo, valor)
        ocorrencia.atualizado_em = datetime.now()
        db.session.commit()
        flash("Ocorrência atualizada com sucesso.", "sucesso")
        return redirect(url_for("ocorrencias.detalhe", id=ocorrencia.id))

    return _render_formulario("Editar ocorrência", ocorrencia.como_formulario(), ocorrencia=ocorrencia)


@bp.post("/ocorrencias/<int:id>/excluir")
def excluir(id):
    """Exclui uma ocorrência (a confirmação é feita no navegador, em app.js)."""
    ocorrencia = db.get_or_404(Ocorrencia, id)
    db.session.delete(ocorrencia)
    db.session.commit()
    flash("Ocorrência excluída.", "sucesso")
    return redirect(url_for("ocorrencias.listar"))
