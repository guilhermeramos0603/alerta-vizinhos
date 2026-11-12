"""Testes de integração: simulam o navegador usando as telas do sistema."""
from datetime import datetime, timedelta

from app.models import Ocorrencia, db
from tests.conftest import form_valido


def texto(resposta):
    return resposta.get_data(as_text=True)


def test_lista_vazia(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "Nenhuma ocorrência encontrada." in texto(resposta)


def test_registrar_ocorrencia_valida(client, app):
    resposta = client.post("/ocorrencias/nova", data=form_valido(), follow_redirects=True)
    assert resposta.status_code == 200
    assert "Ocorrência registrada com sucesso." in texto(resposta)
    assert "Estrada da Colônia, km 3" in texto(resposta)
    assert "Anônimo" in texto(resposta)
    with app.app_context():
        assert db.session.query(Ocorrencia).count() == 1


def test_registrar_ocorrencia_invalida_mostra_erros_e_nao_grava(client, app):
    resposta = client.post("/ocorrencias/nova", data=form_valido(descricao="curto", local=""))
    assert resposta.status_code == 400
    assert "Descreva a ocorrência com pelo menos 10 caracteres." in texto(resposta)
    assert "Informe o local da ocorrência." in texto(resposta)
    with app.app_context():
        assert db.session.query(Ocorrencia).count() == 0


def test_filtrar_por_tipo(client, criar_ocorrencia):
    criar_ocorrencia(tipo="Furto", local="Galpão A")
    criar_ocorrencia(tipo="Vandalismo", local="Ponto de ônibus")
    resposta = client.get("/?tipo=Vandalismo")
    assert "Ponto de ônibus" in texto(resposta)
    assert "Galpão A" not in texto(resposta)


def test_filtrar_por_periodo(client, criar_ocorrencia):
    criar_ocorrencia(local="Recente", data_ocorrencia=datetime.now() - timedelta(days=1))
    criar_ocorrencia(local="Antiga", data_ocorrencia=datetime.now() - timedelta(days=60))
    de = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    resposta = client.get(f"/?de={de}")
    assert "Recente" in texto(resposta)
    assert "Antiga" not in texto(resposta)


def test_periodo_invertido_mostra_aviso(client):
    resposta = client.get("/?de=2026-10-30&ate=2026-10-01")
    assert "A data inicial é maior que a data final" in texto(resposta)


def test_detalhe_mostra_os_dados(client, criar_ocorrencia):
    id_ = criar_ocorrencia(local="Galpão do Sr. João")
    resposta = client.get(f"/ocorrencias/{id_}")
    assert resposta.status_code == 200
    assert "Galpão do Sr. João" in texto(resposta)
    assert "Maria" in texto(resposta)


def test_editar_ocorrencia(client, app, criar_ocorrencia):
    id_ = criar_ocorrencia()
    resposta = client.post(f"/ocorrencias/{id_}/editar",
                           data=form_valido(local="Local corrigido"), follow_redirects=True)
    assert "Ocorrência atualizada com sucesso." in texto(resposta)
    with app.app_context():
        assert db.session.get(Ocorrencia, id_).local == "Local corrigido"


def test_editar_com_dados_invalidos_nao_altera(client, app, criar_ocorrencia):
    id_ = criar_ocorrencia(local="Local original")
    resposta = client.post(f"/ocorrencias/{id_}/editar", data=form_valido(local=""))
    assert resposta.status_code == 400
    with app.app_context():
        assert db.session.get(Ocorrencia, id_).local == "Local original"


def test_excluir_ocorrencia(client, app, criar_ocorrencia):
    id_ = criar_ocorrencia()
    resposta = client.post(f"/ocorrencias/{id_}/excluir", follow_redirects=True)
    assert "Ocorrência excluída." in texto(resposta)
    with app.app_context():
        assert db.session.get(Ocorrencia, id_) is None


def test_ocorrencia_inexistente_retorna_404(client):
    resposta = client.get("/ocorrencias/9999")
    assert resposta.status_code == 404
    assert "Página não encontrada" in texto(resposta)


def test_excluir_por_get_nao_e_permitido(client, criar_ocorrencia):
    id_ = criar_ocorrencia()
    resposta = client.get(f"/ocorrencias/{id_}/excluir")
    assert resposta.status_code == 405
