# Tutorial: Como Manter suas Branches Git Locais Sincronizadas

Guia prático para limpar branches locais no Git: remova branches já deletadas no remoto e branches apenas locais, mantendo o repositório organizado.

Atualizado em: 2025-08-06 • Versão: 1.0

Sumário

- [Cenário Comum](#cenário-comum)
- [1. Removendo Branches Locais que Foram Deletadas no Remoto](#1-removendo-branches-locais-que-foram-deletadas-no-remoto)
- [2. Removendo Todas as Branches que São Apenas Locais (Automático)](#2-removendo-todas-as-branches-que-são-apenas-locais-automático)

Este tutorial explica como limpar seu repositório local, removendo branches que não existem mais no repositório remoto (GitHub) ou que foram criadas apenas localmente e nunca enviadas.

## Cenário Comum

Com o tempo, é comum que o repositório local acumule branches que já foram mescladas e deletadas no GitHub. Manter o ambiente local limpo facilita a navegação e evita confusão.

Existem dois tipos de branches "extras" que você pode querer remover:

1.  **Branches que existiam no remoto, mas foram deletadas lá**: Seu Git local ainda "lembra" delas.
2.  **Branches que só existem localmente**: Foram criadas para testes ou trabalho local e nunca foram enviadas para o remoto.

A seguir, apresentamos os comandos para lidar com cada caso.

---

## 1. Removendo Branches Locais que Foram Deletadas no Remoto

Este comando sincroniza seu repositório com o remoto e remove as branches locais que o Git sabe que foram deletadas no GitHub.

### Comando (PowerShell)

```powershell
git fetch -p; git branch -vv | Where-Object { $_ -match ": gone]" } | ForEach-Object { $_.Trim().Split(' ')[0] } | ForEach-Object { if ($_.Length -gt 0) { git branch -d $_ } }
```

### Como Funciona

- `git fetch -p`: O `-p` (ou `--prune`) atualiza seu repositório e remove as referências de rastreamento para branches que não existem mais no remoto.
- `git branch -vv | ...`: O restante do comando filtra a lista de branches para encontrar aquelas marcadas como `[gone]` (desaparecidas) e as remove com `git branch -d`.

---

## 2. Removendo Todas as Branches que São Apenas Locais (Automático)

Este comando é mais abrangente. Ele remove **todas** as branches que não possuem um vínculo com uma branch remota, exceto a branch em que você está no momento (marcada com `*`).

### Comando (PowerShell)

```powershell
git branch -vv | Where-Object { ($_ -notmatch '\[') -and ($_ -notmatch '\*') } | ForEach-Object { $_.Trim().Split(' ')[0] } | ForEach-Object { if ($_.Length -gt 0) { git branch -D $_ } }
```

### Como Funciona

- `git branch -vv`: Lista todas as branches locais com detalhes de rastreamento.
- `Where-Object { ... }`: Filtra essa lista para encontrar branches que:
  - **Não** possuem um vínculo remoto (a linha não contém `[`).
  - E **não** são a sua branch atual (a linha não contém `*`).
- `ForEach-Object { ... }`: Pega o nome de cada branch filtrada e a remove com `git branch -D`. Usamos `-D` (maiúsculo) para forçar a exclusão, já que essas branches podem ter commits que nunca foram enviados ao remoto.

---

Combinando esses dois comandos, você pode manter seu ambiente de desenvolvimento local sempre limpo e sincronizado com o estado atual do seu projeto no GitHub.
