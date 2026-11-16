# Laudo de qualidade

Sistema avaliado: **Alerta Vizinhos**, versão de 15/11/2026 (commit [`2b38712`](https://github.com/guilhermeramos0603/alerta-vizinhos/commit/2b38712)).
Versão corrigida: 16/11/2026 (commits [`c48f557`](https://github.com/guilhermeramos0603/alerta-vizinhos/commit/c48f557), [`8825935`](https://github.com/guilhermeramos0603/alerta-vizinhos/commit/8825935) e [`7735f74`](https://github.com/guilhermeramos0603/alerta-vizinhos/commit/7735f74)).

O laudo junta as duas frentes de teste do projeto:

- **Verificação:** testes automatizados com pytest, que conferem se o código faz o que a especificação (requisitos e regras de negócio) pede.
- **Validação:** cinco pessoas usaram o sistema como usuários, seguindo o [formulário de teste](formulario-de-teste.md), e relataram o que funcionou, o que falhou e o que não testaram.

As respostas completas dos testadores ficam fora do repositório, porque contêm nomes de terceiros. Elas foram entregues em PDF junto com o trabalho. Aqui, cada testador aparece com o primeiro nome e a inicial do sobrenome.

## 1. Testes com usuários (validação)

| # | Testador | Perfil | Data | Dispositivo e navegador |
|---|---|---|---|---|
| 1 | Larissa M. | Colega de curso | 15/11/2026 | Celular Android (Samsung A15), Chrome |
| 2 | Rafael C. | Colega de curso | 15/11/2026 | Notebook Windows 11, Chrome |
| 3 | Marcelo S. | Profissional (desenvolvedor back-end) | 15/11/2026 | Computador Ubuntu, Firefox |
| 4 | Juliana N. | Profissional (QA) | 16/11/2026 | Computador macOS, Chrome, e modo celular do DevTools |
| 5 | Beatriz A. | Colega de curso | 16/11/2026 | iPhone 11, Safari |

### Cobertura: o que cada pessoa testou

`OK` = testou e funcionou · `Falha (Pnn)` = testou e encontrou o problema Pnn · `—` = não testou

| Funcionalidade | Larissa | Rafael | Marcelo | Juliana | Beatriz |
|---|---|---|---|---|---|
| Registrar ocorrência | Falha (P01) | OK | OK | Falha (P01) | OK |
| Mensagens de erro e validação | OK | Falha (P06, P08) | OK | Falha (P06, P07) | OK |
| Lista de ocorrências | OK | OK | OK | Falha (P05) | OK |
| Filtro por tipo | OK | OK | OK | OK | OK |
| Filtro por período | — | OK | OK | OK | — |
| Detalhes | Falha (P11) | OK | OK | Falha (P09) | OK |
| Editar | OK | OK | OK | OK | OK |
| Excluir com confirmação | OK | OK | OK | OK | — |
| Uso no celular | Falha (P12) | — | — | OK (simulado) | OK |
| Segurança (HTML/JS, SQL, URL manipulada, 404, 405) | — | — | Falha (P02, P03, P04, P10, P13) | — | — |

**Funcionalidades não testadas e por quê**

- Larissa não testou o filtro por período (teve que parar no meio do teste) nem o computador. O filtro por período foi coberto por Rafael, Marcelo e Juliana.
- Rafael e Marcelo não testaram no celular. O celular foi coberto por Larissa, Beatriz e Juliana.
- Beatriz não testou a exclusão, com medo de apagar a ocorrência de outro colega, já que não há login. Esse receio confirma o problema P03.
- Ninguém fez teste de carga. Marcelo evitou de propósito, para não encher de registros falsos o banco usado pelos outros. O risco de spam ficou registrado como P13.
- Ninguém testou a acessibilidade com leitor de tela. Fica registrado como lacuna para a próxima rodada.

## 2. Problemas encontrados e correções

Critério de gravidade: **Alta**, quando compromete a segurança ou a integridade dos dados. **Média**, quando gera dado errado ou duplicado ou atrapalha o uso. **Baixa**, quando é mensagem, aparência ou conveniência.

| ID | Encontrado por | Problema | Gravidade | Correção realizada | Evidência | Situação |
|---|---|---|---|---|---|---|
| P01 | Larissa, Juliana | Dois cliques (ou toques) seguidos em Salvar gravavam a mesma ocorrência duas vezes. | Média | O botão Salvar trava depois do primeiro envio e mostra "Salvando..." (`app/static/app.js`). Se a pessoa voltar pela seta do navegador, o botão é liberado de novo. | `c48f557` · [antes](evidencias/antes-05-envio-duplicado.png) · [depois](evidencias/depois-05-botao-salvando.png) · [2 cliques = 1 registro](evidencias/depois-05b-duplo-clique-um-registro.png) | Corrigido |
| P02 | Marcelo | Os formulários não tinham proteção contra CSRF: outro site conseguia enviar um POST de exclusão usando o navegador de quem estava com o sistema aberto. | Alta | Flask-WTF (`CSRFProtect`): todos os formulários levam um token, e envio sem token mostra a página "Formulário expirado". | `c48f557` · `test_csrf.py` (2 testes) · [depois](evidencias/depois-09-csrf.png) | Corrigido |
| P03 | Marcelo (e Beatriz) | Não há login: qualquer pessoa com o link pode editar ou excluir qualquer ocorrência. | Alta | Não corrigido nesta versão: exige cadastro de usuários, que está fora do escopo definido na Situação 1. Ficou como primeira prioridade da próxima versão (código de acesso do grupo, sugestão do Marcelo) e como limitação na [documentação de segurança](../situacao-1/06-configuracao-seguranca-lgpd.md). | — | Não corrigido (próxima versão) |
| P04 | Marcelo | O campo "Seu nome" é texto livre, então dá para registrar em nome de outro vizinho. | Média | Não corrigido: depende do login (P03). | — | Não corrigido (próxima versão) |
| P05 | Juliana | A lista era ordenada pela data em que a ocorrência aconteceu. Um registro feito hoje sobre algo de 3 semanas atrás ia parar no fim da lista e ninguém via. | Média | A lista passou a ser ordenada pela data de registro, e as ocorrências das últimas 24 horas ganharam a marca "Novo". | `c48f557` · `test_lista_mostra_primeiro_as_registradas_mais_recentemente`, `test_ocorrencia_recente_tem_marca_de_novo` · [antes](evidencias/antes-01-lista.png) · [depois](evidencias/depois-01-lista.png) | Corrigido |
| P06 | Rafael, Juliana | O sistema aceitava datas sem sentido, como 01/01/1900. | Baixa | Nova regra: só são aceitas datas dos últimos 12 meses. O campo ganhou os atributos `min` e `max`, então o próprio calendário já não oferece datas fora da janela. | `c48f557` · `test_data_de_1900_e_recusada`, `test_data_mais_antiga_que_12_meses` · [depois](evidencias/depois-07-erros-juntos.png) | Corrigido |
| P07 | Juliana | Com um ano de 5 dígitos (20266), a mensagem era "Informe a data e a hora", mas a data tinha sido informada. | Baixa | Mensagem própria: "Data inválida. Escolha a data e a hora pelo calendário." | `c48f557` · `test_data_invalida_tem_mensagem_propria` | Corrigido |
| P08 | Rafael | A validação era inconsistente: campos vazios eram barrados pelo balão do navegador (um de cada vez) e os outros erros pela caixa do sistema. | Baixa | O formulário passou a usar `novalidate`: todos os erros aparecem juntos, na mesma caixa vermelha do sistema. | `c48f557` · `test_formulario_nao_usa_validacao_do_navegador` · [depois](evidencias/depois-07-erros-juntos.png) | Corrigido |
| P09 | Juliana | Depois de editar, nada indicava que a ocorrência tinha sido alterada. | Baixa | Nova coluna `atualizado_em`. A tela de detalhes mostra "Editado em". | `c48f557` · `test_edicao_registra_data_de_alteracao` · [antes](evidencias/antes-03-detalhe.png) · [depois](evidencias/depois-03-detalhe.png) | Corrigido |
| P10 | Marcelo | Abrir o endereço de exclusão pela barra de endereço mostrava a página padrão do Flask, em inglês ("Method Not Allowed"). | Baixa | Página de erro própria: "Ação não permitida", no visual do sistema. | `c48f557` · `test_excluir_por_get_mostra_pagina_de_erro_do_sistema` · [antes](evidencias/antes-02-erro-405.png) · [depois](evidencias/depois-02-erro-405.png) | Corrigido |
| P11 | Larissa | A mensagem verde de sucesso sumia em 4 segundos, antes de dar tempo de ler. | Baixa | A mensagem fica na tela até a pessoa fechar no ×. | `c48f557` · [depois](evidencias/depois-06-sucesso.png) | Corrigido |
| P12 | Larissa | O primeiro acesso demorou quase 1 minuto para carregar. | Média | Não corrigido no código: o plano gratuito do Render desliga a aplicação depois de 15 minutos sem acesso, e o primeiro acesso seguinte a religa. A mitigação foi avisar na mensagem enviada aos testadores. A solução definitiva é um plano pago de hospedagem. | — | Não corrigido (limitação da hospedagem) |
| P13 | Marcelo | Não há limite de envios: alguém pode cadastrar ocorrências falsas em massa. | Média | Não corrigido nesta versão. Proposta para a próxima: limite de envios por IP com Flask-Limiter. | — | Não corrigido (próxima versão) |

## 3. Sugestões recebidas

| Sugestão | Testador | Decisão |
|---|---|---|
| Botão para compartilhar a ocorrência no WhatsApp | Larissa | Implementada (RF09) |
| Data e hora já preenchidas com o momento atual | Larissa | Implementada |
| Busca por palavra (ex.: "galpão") | Rafael | Implementada (RF08) · [depois](evidencias/depois-08-busca.png) |
| Atributo `max` no campo de data, para o calendário não oferecer o futuro | Juliana | Implementada (junto com P06) |
| Filtro recolhido no celular, para a lista aparecer primeiro | Beatriz | Implementada · [antes](evidencias/antes-04-celular-lista.png) · [depois](evidencias/depois-04-celular-lista.png) |
| Cartão inteiro clicável, não só o link "Ver detalhes" | Beatriz | Implementada |
| Uma cor para cada tipo de ocorrência | Beatriz | Implementada |
| Letra maior | Beatriz | Implementada em parte: rótulos dos campos e datas passaram de 14 para 15 px |
| Paginação ou "carregar mais" | Rafael | Versão futura: o volume atual de registros é pequeno |
| Resumo mensal por tipo | Rafael | Versão futura |
| Código de acesso do grupo, ou só quem criou poder editar | Marcelo | Versão futura, prioridade 1 (resolve P03 e P04) |
| Exclusão lógica e histórico de alterações | Marcelo | Versão futura |
| Limite de envios por IP | Marcelo | Versão futura (resolve P13) |
| Mapa da colônia e aviso no WhatsApp a cada novo registro | Beatriz | Versão futura (já estava fora do escopo) |

## 4. Testes automatizados (verificação)

| | Antes das correções (`2b38712`) | Depois das correções (`8825935`) |
|---|---|---|
| Testes unitários (`test_modelo.py`) | 9 | 13 |
| Testes de integração (`test_rotas.py`, `test_csrf.py`) | 12 | 23 |
| **Total** | **21, todos aprovados** | **36, todos aprovados** |

Cada correção ganhou pelo menos um teste novo, citado na coluna "Evidência" da tabela acima. Assim, se o problema voltar no futuro, o pytest acusa.

- [Saída do pytest antes das correções](evidencias/testes-antes.png)
- [Saída do pytest depois das correções](evidencias/testes-depois.png)

## 5. Conclusão

Os cinco testadores encontraram 13 problemas: 2 de gravidade alta, 5 de gravidade média e 6 de gravidade baixa. Nove foram corrigidos em 16/11/2026, e cada correção tem um teste automatizado que a confirma. Os quatro problemas restantes ficaram para a próxima versão. Três deles (falta de login, nome em texto livre e falta de limite de envios) exigem controle de acesso, que está fora do escopo desta versão. O quarto (demora no primeiro acesso) é uma limitação do plano gratuito de hospedagem. Das 14 sugestões recebidas, 8 foram implementadas. O sistema termina esta rodada com as funções do escopo funcionando, 36 testes automatizados aprovados e as limitações conhecidas documentadas.
