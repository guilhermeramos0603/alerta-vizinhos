# 1. Escopo e requisitos

> Observação: o material do Projeto Integrador I (2025/1) não está mais disponível. Por isso, a documentação de planejamento foi refeita nesta etapa, conforme permite a Situação-Problema 1 ("verifique e adeque seu escopo/ideia").

## Situação-problema

Na Colônia Dom Pedro II, área rural de Campo Largo/PR, as propriedades são grandes e distantes umas das outras. Furtos de ferramentas, combustível, implementos agrícolas, fiação de cobre e animais acontecem sem que os vizinhos fiquem sabendo a tempo, e as informações circulam soltas no grupo de WhatsApp, onde se perdem no meio de outras mensagens.

## Objetivo

Oferecer ao grupo de vizinhos um lugar único para **registrar e consultar ocorrências de segurança**, de forma simples e pelo celular, para que todos saibam o que aconteceu, onde e quando.

## Público-alvo

Moradores e pequenos produtores rurais da Colônia Dom Pedro II, a maioria com pouca familiaridade com tecnologia.

## Escopo

**Dentro do escopo (esta versão):**
- Registrar uma ocorrência (tipo, data e hora, local, descrição e, opcionalmente, o nome de quem registra).
- Listar as ocorrências, das registradas mais recentemente para as mais antigas, destacando as das últimas 24 horas.
- Filtrar a lista por tipo e por período e buscar por palavra.
- Ver os detalhes, editar e excluir uma ocorrência.
- Compartilhar uma ocorrência no WhatsApp.

**Fora do escopo (versões futuras):**
- Login e controle de quem pode editar ou excluir.
- Mapa das propriedades.
- Notificações automáticas (WhatsApp, SMS, e-mail).
- Envio de fotos.

## Requisitos funcionais

| Código | Requisito |
|---|---|
| RF01 | O sistema deve permitir registrar uma ocorrência com tipo, data e hora, local, descrição e nome (opcional). |
| RF02 | O sistema deve listar as ocorrências da registrada mais recentemente para a mais antiga, com a marca "Novo" nas registradas nas últimas 24 horas. |
| RF03 | O sistema deve permitir filtrar as ocorrências por tipo. |
| RF04 | O sistema deve permitir filtrar as ocorrências por período (data inicial e final). |
| RF05 | O sistema deve exibir os detalhes de uma ocorrência. |
| RF06 | O sistema deve permitir editar uma ocorrência. |
| RF07 | O sistema deve permitir excluir uma ocorrência, pedindo confirmação antes. |
| RF08 | O sistema deve permitir buscar ocorrências por uma palavra do local ou da descrição. |
| RF09 | O sistema deve permitir compartilhar uma ocorrência no WhatsApp. |
| RF10 | O sistema deve mostrar quando uma ocorrência foi editada. |

## Requisitos não funcionais

| Código | Requisito |
|---|---|
| RNF01 | Interface responsiva, utilizável no celular. |
| RNF02 | Linguagem simples, sem termos técnicos. |
| RNF03 | Back-end em Python, no padrão MVC. |
| RNF04 | Dados armazenados em PostgreSQL. |
| RNF05 | Sistema publicado na internet, acessível por um link. |
| RNF06 | Erros de preenchimento devem ser explicados ao usuário, todos juntos, sem travar o sistema. |
| RNF07 | Os formulários devem ser protegidos contra CSRF e contra envio duplicado. |

## Regras de negócio

| Código | Regra |
|---|---|
| RN01 | O tipo deve ser um destes: Furto, Tentativa de furto, Movimentação suspeita, Vandalismo ou Outro. |
| RN02 | A descrição deve ter entre 10 e 1000 caracteres. |
| RN03 | O local é obrigatório (até 120 caracteres). |
| RN04 | A data da ocorrência não pode estar no futuro nem ser anterior a 12 meses. |
| RN05 | Se o nome não for informado, a ocorrência é registrada como "Anônimo". |
