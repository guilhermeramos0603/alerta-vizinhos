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
| Exclusão por link | A exclusão só aceita POST e pede confirmação antes. Abrir o endereço de exclusão direto mostra a página de erro do sistema (405). |
| CSRF (formulário enviado por outro site) | Todos os formulários levam um token gerado pelo Flask-WTF (`CSRFProtect`); envio sem o token é recusado. |
| Envio duplicado | O botão Salvar trava depois do primeiro clique. |
| Senhas e chaves no código | A URL do banco e a chave secreta ficam em variáveis de ambiente, fora do repositório. |

**Limitações conhecidas (versões futuras):**
- Não há login: qualquer pessoa com o link pode editar ou excluir ocorrências (problema P03 do [laudo de qualidade](../situacao-3/laudo-de-qualidade.md)).
- O nome é texto livre, então é possível registrar em nome de outra pessoa (depende do login).
- Não há limite de envios por pessoa (proteção contra spam).
- A exclusão é definitiva, sem histórico para recuperar.

## LGPD

- O sistema coleta o mínimo de dados pessoais: apenas o nome, e de forma opcional.
- Não são coletados CPF, telefone, endereço ou e-mail.
- Quem não quiser se identificar pode registrar como "Anônimo".
