# Manual de uso

O Alerta Vizinhos funciona pelo navegador, no celular ou no computador. Não precisa instalar nada nem criar conta.

> No plano gratuito do Render, o primeiro acesso depois de um tempo parado pode levar até 1 minuto para carregar. Depois disso, o sistema fica rápido.

## Registrar uma ocorrência

1. Clique em **+ Registrar**, no topo da tela.
2. Escolha o **tipo** (Furto, Tentativa de furto, Movimentação suspeita, Vandalismo ou Outro).
3. Informe a **data e a hora** em que aconteceu.
4. Escreva o **local** (por exemplo, "Estrada da Colônia, perto do galpão do Sr. João").
5. Descreva **o que aconteceu**, com pelo menos 10 caracteres.
6. Se quiser, escreva **seu nome**. Em branco, a ocorrência fica como "Anônimo".
7. Clique em **Salvar**.

Se algum campo estiver errado, o sistema mostra o que precisa ser corrigido e mantém o que você já digitou.

## Consultar e filtrar

A página inicial mostra todas as ocorrências, das mais recentes para as mais antigas. Para filtrar, escolha o tipo e/ou as datas **De** e **Até** e clique em **Filtrar**. **Limpar** volta a mostrar tudo.

## Ver, editar e excluir

Clique em **Ver detalhes** em uma ocorrência. Na tela de detalhes:
- **Editar** abre o formulário já preenchido.
- **Excluir** pede confirmação antes de apagar.

## Executar no computador (para desenvolvedores)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wsgi.py          # abre em http://127.0.0.1:5000
pytest                  # roda os testes automatizados
```

Sem a variável `DATABASE_URL`, o sistema usa um arquivo SQLite local.
