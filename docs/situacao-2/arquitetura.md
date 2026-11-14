# Arquitetura da solução

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem do back-end | Python 3.12 com Flask |
| Acesso a dados | SQLAlchemy (ORM) |
| Banco de dados | PostgreSQL (Neon) |
| Front-end | HTML (templates Jinja), CSS e JavaScript puro |
| Testes | pytest |
| Hospedagem | Render (aplicação) e Neon (banco) |
| Modo de codificação | Tradicional |

## Padrão MVC

```mermaid
flowchart LR
    U[Usuário] -- "requisição HTTP" --> C[Controller<br/>app/controllers.py]
    C -- "valida / consulta / grava" --> M[Model<br/>app/models.py]
    M <--> BD[(PostgreSQL)]
    C -- "dados" --> V[View<br/>app/templates/*.html]
    V -- "HTML" --> U
```

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| Model | `app/models.py` | Entidade `Ocorrencia`, regras de validação e mapeamento para a tabela |
| View | `app/templates/*.html`, `app/static/` | Telas em HTML, estilo (CSS) e comportamentos simples (JS) |
| Controller | `app/controllers.py` | Rotas: listar, registrar, detalhar, editar e excluir |
| Configuração | `app/__init__.py`, `wsgi.py` | Cria a aplicação, conecta o banco e trata erros 404 e 500 |

## Rotas

| Método | Endereço | Ação |
|---|---|---|
| GET | `/` | Lista e filtra as ocorrências (`?tipo=`, `?de=`, `?ate=`) |
| GET, POST | `/ocorrencias/nova` | Formulário e cadastro |
| GET | `/ocorrencias/<id>` | Detalhes |
| GET, POST | `/ocorrencias/<id>/editar` | Formulário e edição |
| POST | `/ocorrencias/<id>/excluir` | Exclusão |

## Tratamento de erros

- Dados inválidos: o formulário volta com a lista de erros e com o que já tinha sido digitado (HTTP 400).
- Ocorrência inexistente: página "Página não encontrada" (HTTP 404).
- Falha inesperada: a transação do banco é desfeita e aparece a página "Erro interno" (HTTP 500).

## Testes automatizados

21 testes em `tests/`:
- `test_modelo.py`: testes unitários das regras de validação (RN01 a RN05).
- `test_rotas.py`: testes de integração que simulam o uso das telas (cadastro, lista, filtros, edição, exclusão e erros).
