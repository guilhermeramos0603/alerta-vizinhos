# 3. Modelagem UML

Os diagramas estão em Mermaid, que o GitHub desenha automaticamente ao abrir este arquivo.

## Diagrama de casos de uso

```mermaid
flowchart LR
    morador(["👤 Morador"])
    subgraph Sistema Alerta Vizinhos
        uc1(("Registrar ocorrência"))
        uc2(("Consultar ocorrências"))
        uc3(("Filtrar por tipo e período"))
        uc4(("Ver detalhes"))
        uc5(("Editar ocorrência"))
        uc6(("Excluir ocorrência"))
        uc7(("Buscar por palavra"))
        uc8(("Compartilhar no WhatsApp"))
    end
    morador --- uc1
    morador --- uc2
    morador --- uc4
    morador --- uc5
    morador --- uc6
    uc3 -. "extend" .-> uc2
    uc7 -. "extend" .-> uc2
    uc8 -. "extend" .-> uc4
```

## Caso de uso expandido: Registrar ocorrência

| Item | Descrição |
|---|---|
| Ator | Morador |
| Pré-condição | Nenhuma (o sistema não exige login nesta versão). A data e a hora já vêm preenchidas com o momento atual. |
| Fluxo principal | 1. O morador clica em "+ Registrar". 2. O sistema mostra o formulário. 3. O morador preenche tipo, data e hora, local, descrição e, se quiser, o nome. 4. O morador clica em "Salvar". 5. O sistema valida os dados e grava a ocorrência. 6. O sistema mostra os detalhes com a mensagem "Ocorrência registrada com sucesso." |
| Fluxo alternativo A | No passo 5, se algum dado for inválido, o sistema mostra todos os erros juntos e mantém o que já foi digitado. |
| Fluxo alternativo C | No passo 4, o botão Salvar fica travado depois do primeiro clique, evitando registros duplicados. |
| Fluxo alternativo B | No passo 3, se o nome ficar em branco, a ocorrência é gravada como "Anônimo". |
| Pós-condição | A ocorrência aparece na lista. |

## Diagrama de classes

```mermaid
classDiagram
    class Ocorrencia {
        +int id
        +str tipo
        +str descricao
        +str local
        +datetime data_ocorrencia
        +str registrado_por
        +datetime criado_em
        +datetime atualizado_em
        +classe_tipo() str
        +eh_nova() bool
        +validar(dados) tuple$
        +como_formulario() dict
    }
    class ControllerOcorrencias {
        +listar()
        +nova()
        +detalhe(id)
        +editar(id)
        +excluir(id)
    }
    ControllerOcorrencias ..> Ocorrencia : usa
```

## Diagrama de sequência: Registrar ocorrência

```mermaid
sequenceDiagram
    actor M as Morador
    participant V as View (form.html)
    participant C as Controller (nova)
    participant O as Model (Ocorrencia)
    participant BD as PostgreSQL
    M->>V: preenche e clica em Salvar
    V->>C: POST /ocorrencias/nova
    C->>O: validar(dados)
    alt dados inválidos
        O-->>C: lista de erros
        C-->>V: formulário com erros (400)
    else dados válidos
        O-->>C: dados limpos
        C->>BD: INSERT ocorrencia
        BD-->>C: id gerado
        C-->>M: redireciona para os detalhes + mensagem de sucesso
    end
```

## Diagrama de atividades: Registrar ocorrência

```mermaid
flowchart TD
    A([Início]) --> B[Abrir formulário]
    B --> C[Preencher dados]
    C --> D[Clicar em Salvar]
    D --> E{Dados válidos?}
    E -- Não --> F[Mostrar erros mantendo o que foi digitado] --> C
    E -- Sim --> G{Nome informado?}
    G -- Não --> H[Usar 'Anônimo'] --> I
    G -- Sim --> I[Gravar no banco]
    I --> J[Mostrar detalhes com mensagem de sucesso]
    J --> K([Fim])
```
