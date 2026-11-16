"""Cria e configura a aplicação Flask."""
import os

from flask import Flask, render_template

from .models import db


def _url_do_banco():
    """Lê a URL do banco na variável DATABASE_URL (PostgreSQL em produção).

    Sem a variável, usa um arquivo SQLite local, só para desenvolvimento.
    """
    url = os.environ.get("DATABASE_URL", "sqlite:///alerta_vizinhos.db")
    # Os provedores entregam "postgres://" ou "postgresql://"; o driver psycopg 3 usa "postgresql+psycopg://".
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=_url_do_banco(),
        SECRET_KEY=os.environ.get("SECRET_KEY", "apenas-para-desenvolvimento"),
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    from .controllers import bp
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def nao_encontrado(_erro):
        return render_template(
            "erro.html",
            titulo="Página não encontrada",
            mensagem="O endereço acessado não existe ou a ocorrência foi excluída.",
        ), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        db.session.rollback()
        return render_template(
            "erro.html",
            titulo="Erro interno",
            mensagem="Algo deu errado ao processar o pedido. Tente novamente em instantes.",
        ), 500

    with app.app_context():
        db.create_all()

    return app
