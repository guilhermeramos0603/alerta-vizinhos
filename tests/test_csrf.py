"""Testes da proteção contra CSRF (ligada, como em produção)."""
import pytest

from app import create_app
from app.models import db
from tests.conftest import form_valido


@pytest.fixture
def client_com_csrf():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": True,
                      "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    yield app.test_client()
    with app.app_context():
        db.drop_all()


def test_envio_sem_token_e_recusado(client_com_csrf):
    resposta = client_com_csrf.post("/ocorrencias/nova", data=form_valido())
    assert resposta.status_code == 400
    assert "Formulário expirado" in resposta.get_data(as_text=True)


def test_formulario_traz_o_token(client_com_csrf):
    assert 'name="csrf_token"' in client_com_csrf.get("/ocorrencias/nova").get_data(as_text=True)
