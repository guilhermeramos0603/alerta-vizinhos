"""Testes unitários das regras de validação do Model."""
from datetime import datetime, timedelta

from app.models import Ocorrencia
from tests.conftest import form_valido


def test_dados_validos_nao_geram_erros():
    dados, erros = Ocorrencia.validar(form_valido())
    assert erros == []
    assert dados["tipo"] == "Movimentação suspeita"
    assert isinstance(dados["data_ocorrencia"], datetime)


def test_nome_em_branco_vira_anonimo():
    dados, erros = Ocorrencia.validar(form_valido(registrado_por="   "))
    assert erros == []
    assert dados["registrado_por"] == "Anônimo"


def test_tipo_invalido():
    _, erros = Ocorrencia.validar(form_valido(tipo="Assalto a banco"))
    assert "Selecione um tipo de ocorrência válido." in erros


def test_descricao_curta_demais():
    _, erros = Ocorrencia.validar(form_valido(descricao="furto"))
    assert "Descreva a ocorrência com pelo menos 10 caracteres." in erros


def test_descricao_longa_demais():
    _, erros = Ocorrencia.validar(form_valido(descricao="x" * 1001))
    assert "A descrição pode ter no máximo 1000 caracteres." in erros


def test_local_obrigatorio():
    _, erros = Ocorrencia.validar(form_valido(local="  "))
    assert "Informe o local da ocorrência." in erros


def test_data_vazia():
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia=""))
    assert "Informe a data e a hora da ocorrência." in erros


def test_data_invalida_tem_mensagem_propria():
    # Ex.: ano com 5 dígitos digitado no campo de data do Chrome
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia="20266-11-16T10:00"))
    assert "Data inválida. Escolha a data e a hora pelo calendário." in erros
    assert "Informe a data e a hora da ocorrência." not in erros


def test_data_mais_antiga_que_12_meses():
    antiga = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%dT%H:%M")
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia=antiga))
    assert "A data da ocorrência deve estar dentro dos últimos 12 meses." in erros


def test_data_de_1900_e_recusada():
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia="1900-01-01T10:00"))
    assert "A data da ocorrência deve estar dentro dos últimos 12 meses." in erros


def test_data_de_11_meses_atras_e_aceita():
    dentro = (datetime.now() - timedelta(days=330)).strftime("%Y-%m-%dT%H:%M")
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia=dentro))
    assert erros == []


def test_data_no_futuro():
    amanha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia=amanha))
    assert "A data da ocorrência não pode estar no futuro." in erros


def test_espacos_extras_sao_removidos():
    dados, erros = Ocorrencia.validar(form_valido(local="  Galpão  "))
    assert erros == []
    assert dados["local"] == "Galpão"
