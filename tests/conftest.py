from datetime import datetime, timedelta

import pytest

from app import create_app
from app.models import Ocorrencia, db


@pytest.fixture
def app():
    """Aplicação de teste com banco SQLite em memória (some ao fim de cada teste)."""
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False,
                      "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def criar_ocorrencia(app):
    """Grava uma ocorrência direto no banco e devolve o id dela."""
    def _criar(**campos):
        dados = {
            "tipo": "Furto",
            "descricao": "Levaram a motobomba do galpão durante a madrugada.",
            "local": "Galpão do Sr. João",
            "data_ocorrencia": datetime.now() - timedelta(days=1),
            "registrado_por": "Maria",
        }
        dados.update(campos)
        with app.app_context():
            ocorrencia = Ocorrencia(**dados)
            db.session.add(ocorrencia)
            db.session.commit()
            return ocorrencia.id
    return _criar


def form_valido(**campos):
    """Dados de formulário válidos, como o navegador envia."""
    dados = {
        "tipo": "Movimentação suspeita",
        "descricao": "Carro desconhecido parado na estrada com farol apagado.",
        "local": "Estrada da Colônia, km 3",
        "data_ocorrencia": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M"),
        "registrado_por": "",
    }
    dados.update(campos)
    return dados
