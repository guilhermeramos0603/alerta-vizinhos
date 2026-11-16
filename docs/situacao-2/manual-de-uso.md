# Manual de uso

O Alerta Vizinhos funciona pelo navegador, no celular ou no computador. Não precisa instalar nada nem criar conta.

> No plano gratuito do Render, o primeiro acesso depois de um tempo parado pode levar até 1 minuto para carregar. Depois disso, o sistema fica rápido.

## Registrar uma ocorrência

1. Clique em **+ Registrar**, no topo da tela.
2. Escolha o **tipo** (Furto, Tentativa de furto, Movimentação suspeita, Vandalismo ou Outro).
3. Confira a **data e a hora**. Elas já vêm com o momento atual; mude se aconteceu antes (até 12 meses atrás).
4. Escreva o **local** (por exemplo, "Estrada da Colônia, perto do galpão do Sr. João").
5. Descreva **o que aconteceu**, com pelo menos 10 caracteres.
6. Se quiser, escreva **seu nome**. Em branco, a ocorrência fica como "Anônimo".
7. Clique em **Salvar**.

Se algum campo estiver errado, o sistema mostra tudo o que precisa ser corrigido de uma vez e mantém o que você já digitou. A mensagem de sucesso fica na tela até você fechar no ×.

## Consultar e filtrar

A página inicial mostra todas as ocorrências, das registradas mais recentemente para as mais antigas. As registradas nas últimas 24 horas têm a marca **Novo**, e cada tipo tem uma cor.

Para filtrar, abra **Filtrar e buscar** (no celular ele fica recolhido), digite uma palavra e/ou escolha o tipo e as datas e clique em **Filtrar**. **Limpar** volta a mostrar tudo.

## Ver, editar e excluir

Toque em qualquer parte do cartão da ocorrência. Na tela de detalhes:
- **Compartilhar no WhatsApp** abre o WhatsApp com um resumo e o link da ocorrência, para mandar no grupo.
- **Editar** abre o formulário já preenchido. Depois de editar, aparece "Editado em" nos detalhes.
- **Excluir** pede confirmação antes de apagar.

## Executar no computador (para desenvolvedores)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app wsgi run --port 5050   # abre em http://127.0.0.1:5050
pytest                  # roda os testes automatizados
```

Sem a variável `DATABASE_URL`, o sistema usa um arquivo SQLite local.
