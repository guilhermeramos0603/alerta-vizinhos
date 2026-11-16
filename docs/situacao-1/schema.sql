-- Projeto físico do banco de dados (PostgreSQL)
-- Gerado a partir do modelo da aplicação (app/models.py)

CREATE TABLE ocorrencia (
    id               SERIAL                      NOT NULL,
    tipo             VARCHAR(30)                 NOT NULL,
    descricao        TEXT                        NOT NULL,
    local            VARCHAR(120)                NOT NULL,
    data_ocorrencia  TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    registrado_por   VARCHAR(80)                 NOT NULL,
    criado_em        TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    atualizado_em    TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);
