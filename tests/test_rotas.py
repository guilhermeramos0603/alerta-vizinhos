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


def test_excluir_por_get_mostra_pagina_de_erro_do_sistema(client, app, criar_ocorrencia):
    id_ = criar_ocorrencia()
    resposta = client.get(f"/ocorrencias/{id_}/excluir")
    assert resposta.status_code == 405
    assert "Ação não permitida" in texto(resposta)
    assert "Method Not Allowed" not in texto(resposta)
    with app.app_context():
        assert db.session.get(Ocorrencia, id_) is not None


def test_lista_mostra_primeiro_as_registradas_mais_recentemente(client, criar_ocorrencia):
    # Registrada antes, mas aconteceu ontem
    criar_ocorrencia(local="Registrada primeiro", data_ocorrencia=datetime.now() - timedelta(days=1),
                     criado_em=datetime.now() - timedelta(hours=2))
    # Registrada agora, mas aconteceu há 3 semanas
    criar_ocorrencia(local="Registrada agora", data_ocorrencia=datetime.now() - timedelta(weeks=3),
                     criado_em=datetime.now())
    pagina = texto(client.get("/"))
    assert pagina.index("Registrada agora") < pagina.index("Registrada primeiro")


def test_ocorrencia_recente_tem_marca_de_novo(client, criar_ocorrencia):
    criar_ocorrencia(criado_em=datetime.now())
    assert ">Novo<" in texto(client.get("/"))


def test_ocorrencia_antiga_nao_tem_marca_de_novo(client, criar_ocorrencia):
    criar_ocorrencia(criado_em=datetime.now() - timedelta(days=3))
    assert ">Novo<" not in texto(client.get("/"))


def test_busca_por_palavra_no_local_e_na_descricao(client, criar_ocorrencia):
    criar_ocorrencia(local="Galpão do Sr. João", descricao="Levaram ferramentas durante a noite.")
    criar_ocorrencia(local="Estrada principal", descricao="Levaram a motobomba do poço.")
    criar_ocorrencia(local="Ponto de ônibus", descricao="Pichação no abrigo do ônibus.")
    resposta = texto(client.get("/?q=motobomba"))
    assert "Estrada principal" in resposta
    assert "Galpão do Sr. João" not in resposta
    resposta = texto(client.get("/?q=galpão"))
    assert "Galpão do Sr. João" in resposta
    assert "Ponto de ônibus" not in resposta


def test_formulario_novo_vem_com_data_e_hora_atuais(client):
    agora = datetime.now().strftime("%Y-%m-%dT%H:")
    assert f'value="{agora}' in texto(client.get("/ocorrencias/nova"))


def test_formulario_nao_usa_validacao_do_navegador(client):
    # Todos os erros aparecem juntos na caixa do sistema (novalidate)
    assert "novalidate" in texto(client.get("/ocorrencias/nova"))


def test_edicao_registra_data_de_alteracao(client, app, criar_ocorrencia):
    id_ = criar_ocorrencia()
    assert "Editado em" not in texto(client.get(f"/ocorrencias/{id_}"))
    client.post(f"/ocorrencias/{id_}/editar", data=form_valido(local="Local corrigido"))
    with app.app_context():
        assert db.session.get(Ocorrencia, id_).atualizado_em is not None
    assert "Editado em" in texto(client.get(f"/ocorrencias/{id_}"))


def test_detalhe_tem_botao_de_compartilhar_no_whatsapp(client, criar_ocorrencia):
    id_ = criar_ocorrencia(local="Galpão do Sr. João")
    pagina = texto(client.get(f"/ocorrencias/{id_}"))
    assert "https://wa.me/?text=" in pagina
    assert "Compartilhar no WhatsApp" in pagina


def test_etiqueta_tem_cor_por_tipo(client, criar_ocorrencia):
    criar_ocorrencia(tipo="Vandalismo")
    assert "tipo-vandalismo" in texto(client.get("/"))
