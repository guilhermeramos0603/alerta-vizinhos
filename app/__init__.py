"""Cria e configura a aplicação Flask."""
import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError, CSRFProtect
from sqlalchemy import inspect, text
from werkzeug.middleware.proxy_fix import ProxyFix

from .models import db

csrf = CSRFProtect()


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


def _atualizar_esquema():
    """Cria as tabelas e acrescenta colunas novas em bancos criados por versões anteriores."""
    db.create_all()
    colunas = {c["name"] for c in inspect(db.engine).get_columns("ocorrencia")}
    if "atualizado_em" not in colunas:
        with db.engine.begin() as conexao:
            conexao.execute(text("ALTER TABLE ocorrencia ADD COLUMN atualizado_em TIMESTAMP"))


def _pagina_de_erro(titulo, mensagem, status):
    return render_template("erro.html", titulo=titulo, mensagem=mensagem), status


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=_url_do_banco(),
        SECRET_KEY=os.environ.get("SECRET_KEY", "apenas-para-desenvolvimento"),
    )
    if config:
        app.config.update(config)

    # No Render, a aplicação fica atrás de um proxy HTTPS; isto faz os links externos saírem com https.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    db.init_app(app)
    csrf.init_app(app)

    from .controllers import bp
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def nao_encontrado(_erro):
        return _pagina_de_erro("Página não encontrada",
                               "O endereço acessado não existe ou a ocorrência foi excluída.", 404)

    @app.errorhandler(405)
    def metodo_nao_permitido(_erro):
        return _pagina_de_erro("Ação não permitida",
                               "Este endereço não pode ser aberto diretamente. Use os botões do sistema.", 405)

    @app.errorhandler(CSRFError)
    def formulario_expirado(_erro):
        return _pagina_de_erro("Formulário expirado",
                               "A página ficou aberta por muito tempo ou veio de outro site. "
                               "Volte, recarregue a página e tente de novo.", 400)

    @app.errorhandler(500)
    def erro_interno(_erro):
        db.session.rollback()
        return _pagina_de_erro("Erro interno",
                               "Algo deu errado ao processar o pedido. Tente novamente em instantes.", 500)

    with app.app_context():
        _atualizar_esquema()

    return app
