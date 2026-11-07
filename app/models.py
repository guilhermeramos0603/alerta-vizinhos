"""Camada MODEL: a entidade Ocorrencia e as regras de validação dos dados."""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

TIPOS = (
    "Furto",
    "Tentativa de furto",
    "Movimentação suspeita",
    "Vandalismo",
    "Outro",
)

FORMATOS_DATA_HORA = ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S")


class Ocorrencia(db.Model):
    """Uma ocorrência de segurança registrada por um morador."""

    __tablename__ = "ocorrencia"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    local = db.Column(db.String(120), nullable=False)
    data_ocorrencia = db.Column(db.DateTime, nullable=False)
    registrado_por = db.Column(db.String(80), nullable=False, default="Anônimo")
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def validar(dados):
        """Valida os dados vindos do formulário.

        Retorna (dados_limpos, erros). Se a lista de erros vier vazia,
        os dados limpos podem ser gravados no banco.
        """
        erros = []
        tipo = (dados.get("tipo") or "").strip()
        descricao = (dados.get("descricao") or "").strip()
        local = (dados.get("local") or "").strip()
        registrado_por = (dados.get("registrado_por") or "").strip() or "Anônimo"
        data_texto = (dados.get("data_ocorrencia") or "").strip()

        if tipo not in TIPOS:
            erros.append("Selecione um tipo de ocorrência válido.")

        if len(descricao) < 10:
            erros.append("Descreva a ocorrência com pelo menos 10 caracteres.")
        elif len(descricao) > 1000:
            erros.append("A descrição pode ter no máximo 1000 caracteres.")

        if not local:
            erros.append("Informe o local da ocorrência.")
        elif len(local) > 120:
            erros.append("O local pode ter no máximo 120 caracteres.")

        if len(registrado_por) > 80:
            erros.append("O nome pode ter no máximo 80 caracteres.")

        data_ocorrencia = None
        for formato in FORMATOS_DATA_HORA:
            try:
                data_ocorrencia = datetime.strptime(data_texto, formato)
                break
            except ValueError:
                continue
        if data_ocorrencia is None:
            erros.append("Informe a data e a hora da ocorrência.")
        elif data_ocorrencia > datetime.now():
            erros.append("A data da ocorrência não pode estar no futuro.")

        limpos = {
            "tipo": tipo,
            "descricao": descricao,
            "local": local,
            "registrado_por": registrado_por,
            "data_ocorrencia": data_ocorrencia,
        }
        return limpos, erros

    def como_formulario(self):
        """Converte a ocorrência para os valores usados no formulário de edição."""
        return {
            "tipo": self.tipo,
            "descricao": self.descricao,
            "local": self.local,
            "registrado_por": self.registrado_por,
            "data_ocorrencia": self.data_ocorrencia.strftime("%Y-%m-%dT%H:%M"),
        }
