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


def test_data_invalida():
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia="ontem à noite"))
    assert "Informe a data e a hora da ocorrência." in erros


def test_data_no_futuro():
    amanha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
    _, erros = Ocorrencia.validar(form_valido(data_ocorrencia=amanha))
    assert "A data da ocorrência não pode estar no futuro." in erros


def test_espacos_extras_sao_removidos():
    dados, erros = Ocorrencia.validar(form_valido(local="  Galpão  "))
    assert erros == []
    assert dados["local"] == "Galpão"
