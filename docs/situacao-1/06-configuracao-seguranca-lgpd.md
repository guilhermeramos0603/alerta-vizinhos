# 6. Gerência de configuração, segurança e LGPD

## Gerência de configuração

- Código e documentação versionados no Git e publicados no GitHub.
- Branch principal `main`; cada correção feita após os testes dos colegas vira um commit separado, citado no laudo de qualidade.
- Dependências com versões fixas em `requirements.txt`.
- Publicação automática no Render a cada envio para o GitHub.

## Segurança

| Ameaça | Como foi tratada |
|---|---|
| Injeção de SQL | Todas as consultas passam pelo ORM SQLAlchemy, que usa parâmetros e não concatena texto. |
| Injeção de HTML/JavaScript | Os templates Jinja escapam automaticamente o conteúdo digitado pelos usuários. |
| Exclusão por link | A exclusão só aceita POST e pede confirmação antes. |
| Senhas e chaves no código | A URL do banco e a chave secreta ficam em variáveis de ambiente, fora do repositório. |

**Limitações conhecidas (versões futuras):** não há login, então qualquer pessoa com o link pode editar ou excluir ocorrências; não há proteção contra CSRF.

## LGPD

- O sistema coleta o mínimo de dados pessoais: apenas o nome, e de forma opcional.
- Não são coletados CPF, telefone, endereço ou e-mail.
- Quem não quiser se identificar pode registrar como "Anônimo".
