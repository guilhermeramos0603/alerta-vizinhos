# Roteiro dos vídeos

## Vídeo 1: solução em funcionamento (mínimo 5 minutos, narrado)

Gravar a tela com o QuickTime (Arquivo → Nova Gravação de Tela) com o microfone ligado. Mire em 6 minutos para ter margem.

| Tempo | O que mostrar | O que falar |
|---|---|---|
| 0:00–0:40 | Página inicial | Apresentação: nome, RGM, disciplina. O problema: furtos na Colônia Dom Pedro II e informações perdidas no WhatsApp. |
| 0:40–1:20 | README no GitHub | Objetivo do sistema, tecnologias (Python, Flask, PostgreSQL, Render) e a organização das pastas por situação-problema. |
| 1:20–3:30 | Sistema no ar | Registrar uma ocorrência; mostrar um erro de validação (descrição curta, data no futuro); lista; filtro por tipo e por período; detalhes; editar; excluir com confirmação. Mostrar rapidamente no celular (ou no modo celular do navegador). |
| 3:30–4:40 | Código | `models.py` (Model e validação), `controllers.py` (rotas), `templates/` (View). Explicar o MVC com o diagrama de `docs/situacao-2/arquitetura.md`. |
| 4:40–5:30 | Terminal | Rodar `pytest` e mostrar os 36 testes passando. Explicar a diferença entre teste unitário e de integração. |
| 5:30–6:00 | Documentação | Passar pelos diagramas UML e pelo dicionário de dados. Encerrar. |

## Vídeo 2: solução atualizada (até 5 minutos)

Gravar depois das correções. Mire em 3 a 4 minutos.

| Tempo | O que mostrar | O que falar |
|---|---|---|
| 0:00–0:30 | Laudo de qualidade | Quantas pessoas testaram e quantos problemas foram encontrados. |
| 0:30–3:00 | Sistema e código | Para cada correção: o problema relatado, o que foi mudado (commit) e o sistema funcionando depois da correção. |
| 3:00–3:30 | Terminal | `pytest` passando após as correções. |
| 3:30–4:00 | Encerramento | O que ficou para uma próxima versão (ex.: login, mapa, notificações). |

Publicar os dois no YouTube como **Não listado** e colar os links no modelo de entrega.
