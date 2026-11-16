# 2. Histórias de usuário e backlog

## Histórias de usuário

**HU01 – Registrar ocorrência**
Como morador, quero registrar uma ocorrência para que os vizinhos saibam o que aconteceu.
- Critérios de aceite: tipo, data e hora, local e descrição são obrigatórios; nome é opcional; ao salvar, vejo uma mensagem de sucesso e os detalhes da ocorrência.

**HU02 – Consultar ocorrências**
Como morador, quero ver a lista de ocorrências recentes para saber o que tem acontecido na região.
- Critérios de aceite: a lista mostra tipo (com uma cor para cada tipo), data, local e um resumo da descrição; as registradas mais recentemente aparecem primeiro, com a marca "Novo" nas últimas 24 horas; o cartão inteiro abre os detalhes; se não houver nenhuma, aparece um aviso.

**HU03 – Filtrar e buscar ocorrências**
Como morador, quero filtrar por tipo e período e buscar por palavra para encontrar um caso específico.
- Critérios de aceite: posso combinar busca, tipo, data inicial e data final; se a data inicial for maior que a final, aparece um aviso; no celular, o filtro fica recolhido para a lista aparecer primeiro.

**HU04 – Ver detalhes e compartilhar**
Como morador, quero abrir uma ocorrência para ler a descrição completa e compartilhá-la no grupo do WhatsApp.

**HU05 – Corrigir uma ocorrência**
Como morador, quero editar uma ocorrência para corrigir informações erradas.
- Critérios de aceite: o formulário vem preenchido; as mesmas validações do cadastro valem para a edição; os detalhes passam a mostrar "Editado em".

**HU06 – Excluir uma ocorrência**
Como morador, quero excluir uma ocorrência registrada por engano.
- Critérios de aceite: o sistema pede confirmação antes de excluir.

## Backlog do produto (priorizado)

| Prioridade | História | Requisitos |
|---|---|---|
| 1 | HU01 – Registrar ocorrência | RF01, RN01–RN05 |
| 2 | HU02 – Consultar ocorrências | RF02 |
| 3 | HU04 – Ver detalhes e compartilhar | RF05, RF09 |
| 4 | HU03 – Filtrar e buscar ocorrências | RF03, RF04, RF08 |
| 5 | HU05 – Corrigir uma ocorrência | RF06, RF10 |
| 6 | HU06 – Excluir uma ocorrência | RF07 |

## Sprint

Por ser um sistema pequeno, todas as histórias foram desenvolvidas em uma única sprint, nesta ordem de prioridade. Definição de pronto: funcionalidade implementada, coberta por teste automatizado e publicada no ambiente online.
