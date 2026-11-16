"""Acrescenta ocorrências de exemplo ao banco, para demonstrar o sistema.

Uso:
    python scripts/popular_exemplos.py
        -> banco SQLite local (pasta instance/)
    DATABASE_URL='postgresql://...' python scripts/popular_exemplos.py
        -> banco do Neon (produção)

Não apaga nada: só acrescenta os exemplos. As datas são calculadas a partir
de agora, então as três primeiras sempre aparecem com a marca "Novo".
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app  # noqa: E402
from app.models import Ocorrencia, db  # noqa: E402

# (registrada há quantas horas, aconteceu quantas horas antes do registro,
#  tipo, local, descrição, nome, editada?)
EXEMPLOS = [
    # Registro atrasado: aconteceu há 3 semanas, mas foi registrado agora (deve aparecer no topo).
    (1, 504, "Furto", "Depósito do sítio na Estrada do Cerne",
     "Registro atrasado: há umas três semanas levaram a roçadeira e um galão de gasolina "
     "do depósito. Só percebi agora, quando fui usar.", "Pedro", False),
    (2, 5, "Furto", "Sítio perto da capela, Estrada da Colônia km 3",
     "Levaram a motobomba do poço e duas enxadas do galpão durante a madrugada. "
     "O cadeado do portão foi cortado com alicate.", "Antônio", False),
    (20, 1, "Movimentação suspeita", "Rua principal, em frente ao mercado",
     "Carro prata sem placa dianteira passou devagar três vezes entre 22h e 23h, "
     "parando na frente das casas com o farol apagado.", "", False),
    (72, 2, "Tentativa de furto", "Chácara ao lado do campo de futebol",
     "Tentaram abrir o portão lateral. O cachorro latiu e a pessoa fugiu pela mata. "
     "Ficaram marcas de alicate na corrente.", "Marta", True),
    (190, 10, "Vandalismo", "Ponto de ônibus da entrada da colônia",
     "Quebraram o vidro do ponto de ônibus e picharam a placa com o nome da colônia.",
     "", False),
    (360, 30, "Furto", "Galpão comunitário da associação",
     "Sumiram dois rolos de fio de cobre que estavam guardados para a reforma "
     "da iluminação do salão.", "Associação de moradores", False),
    (600, 4, "Outro", "Estrada do Cerne, trecho perto da ponte",
     "Lâmpada do poste queimada há uma semana; o trecho fica totalmente escuro "
     "à noite. Pedido de troca já feito à prefeitura.", "", False),
]


def popular():
    app = create_app()
    agora = datetime.now()
    with app.app_context():
        for horas_registro, horas_antes, tipo, local, descricao, nome, editada in EXEMPLOS:
            criado_em = agora - timedelta(hours=horas_registro)
            ocorrencia = Ocorrencia(
                tipo=tipo,
                local=local,
                descricao=descricao,
                registrado_por=nome or "Anônimo",
                data_ocorrencia=(criado_em - timedelta(hours=horas_antes)).replace(second=0, microsecond=0),
                criado_em=criado_em,
            )
            if editada and hasattr(Ocorrencia, "atualizado_em"):
                ocorrencia.atualizado_em = criado_em + timedelta(hours=3)
            db.session.add(ocorrencia)
        db.session.commit()
        print(f"{len(EXEMPLOS)} ocorrências de exemplo gravadas.")


if __name__ == "__main__":
    popular()
