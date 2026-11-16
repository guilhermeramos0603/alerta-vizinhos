# Alerta Vizinhos

Sistema web para o grupo de vizinhos da Colônia Dom Pedro II (Campo Largo/PR) registrar e consultar ocorrências de segurança, como furtos, tentativas de furto e movimentações suspeitas.

Projeto Integrador Transdisciplinar em Engenharia de Software II, de Guilherme Silvano de Ramos.

- **Sistema em funcionamento:** https://alerta-vizinhos.onrender.com
- **Vídeo da solução:** [LINK DO VÍDEO 1]
- **Vídeo da solução atualizada:** [LINK DO VÍDEO 2]

## Funcionalidades

- Registrar ocorrência (tipo, data e hora, local, descrição e nome opcional)
- Listar ocorrências, das registradas mais recentemente para as mais antigas, com a marca "Novo" nas últimas 24 horas
- Buscar por palavra e filtrar por tipo e por período
- Ver detalhes, editar (com "Editado em") e excluir (com confirmação)
- Compartilhar uma ocorrência no WhatsApp
- Validação dos dados com todos os erros explicados juntos
- Proteção contra CSRF e contra envio duplicado
- Layout responsivo, para uso no celular

## Tecnologias

Python 3.12 · Flask · SQLAlchemy · Flask-WTF · PostgreSQL · HTML, CSS e JavaScript · pytest · Render (hospedagem) · Neon (banco)

Arquitetura em camadas no padrão **MVC**. Detalhes em [docs/situacao-2/arquitetura.md](docs/situacao-2/arquitetura.md).

## Organização do repositório

```
app/                 código da aplicação
  models.py          Model: entidade Ocorrencia e validações
  controllers.py     Controller: rotas
  templates/         View: telas HTML
  static/            CSS e JavaScript
tests/               testes automatizados (pytest)
scripts/             popular_exemplos.py: ocorrências de exemplo para demonstração
docs/
  situacao-1/        planejamento: escopo, histórias, UML, IHC, banco de dados, segurança
  situacao-2/        desenvolvimento: arquitetura e manual de uso
  situacao-3/        validação: formulário de teste, laudo de qualidade (com evidências) e roteiro dos vídeos
```

## Documentação

| Situação | Documento |
|---|---|
| 1 | [Escopo e requisitos](docs/situacao-1/01-escopo-e-requisitos.md) |
| 1 | [Histórias de usuário e backlog](docs/situacao-1/02-historias-e-backlog.md) |
| 1 | [Diagramas UML](docs/situacao-1/03-uml.md) |
| 1 | [Interface (IHC) e mapa navegacional](docs/situacao-1/04-interface-ihc.md) |
| 1 | [Banco de dados e dicionário de dados](docs/situacao-1/05-banco-de-dados.md) |
| 1 | [Configuração, segurança e LGPD](docs/situacao-1/06-configuracao-seguranca-lgpd.md) |
| 2 | [Arquitetura](docs/situacao-2/arquitetura.md) |
| 2 | [Manual de uso](docs/situacao-2/manual-de-uso.md) |
| 3 | [Formulário de teste](docs/situacao-3/formulario-de-teste.md) |
| 3 | [Laudo de qualidade](docs/situacao-3/laudo-de-qualidade.md) |

## Executar localmente

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/popular_exemplos.py # opcional: grava 7 ocorrências de exemplo
flask --app wsgi run --port 5050   # http://127.0.0.1:5050 (usa SQLite local)
pytest                             # 36 testes
```

## Publicação

A aplicação roda no Render (plano gratuito), configurada pelo arquivo `render.yaml`. O banco PostgreSQL fica no Neon e é informado pela variável de ambiente `DATABASE_URL`. A tabela é criada automaticamente na primeira execução.
