# 🛠️ Guia Prático: Como manter branches Git locais sincronizadas e limpas

📅 Atualizado em: `2025-08-06` • 🔖 Versão: `1.1`

---

## 📚 Sumário

- [🎯 Contexto e Objetivo](#contexto-e-objetivo)
- [✅ Pré-requisitos](#pré-requisitos)
- [🚶 Passo a passo](#passo-a-passo)
  - [1️⃣ Remover branches locais que foram deletadas no remoto (sincronizar e podar)](#1️⃣-remover-branches-locais-que-foram-deletadas-no-remoto-sincronizar-e-podar)
  - [2️⃣ Remover automaticamente branches que existem apenas localmente](#2️⃣-remover-automaticamente-branches-que-existem-apenas-localmente)
  - [3️⃣ Validar o resultado e revisar o estado](#3️⃣-validar-o-resultado-e-revisar-o-estado)
  - [4️⃣ Opcional: configurar pruning automático e boas práticas](#4️⃣-opcional-configurar-pruning-automático-e-boas-práticas)
- [⚠️ Armadilhas comuns](#armadilhas-comuns)
- [🛠️ Troubleshooting (Erros Comuns)](#troubleshooting-erros-comuns)
- [📎 Referências](#referências)

---

## 🎯 Contexto e Objetivo

Este guia resolve o acúmulo de branches no repositório Git local que:

- Já foram mescladas e deletadas no GitHub (marcadas como [gone]).
- Foram criadas apenas localmente e nunca tiveram tracking remoto.

Resultado esperado:

- Ambiente local limpo, apenas com branches relevantes.
- Remoção segura das referências obsoletas ao remoto.
- Remoção automatizada de branches somente locais (excluindo a branch atual).

Para quem é útil:

- Pessoas desenvolvedoras que mantêm muitos branches.
- Times que desejam padronizar a limpeza do repositório local.

Ao final, você terá executado comandos para sincronizar com o remoto, remover branches obsoletas e configurar pruning automático.

---

## ✅ Pré-requisitos

- ✅ Sistemas operacionais suportados: Windows 10+ (PowerShell), macOS 12+ e Linux (bash/zsh)
- ✅ Git instalado e no PATH:
  - Windows: https://git-scm.com/download/win
  - macOS: https://git-scm.com/download/mac
  - Linux: https://git-scm.com/download/linux
- ✅ Permissões para executar comandos no terminal (PowerShell ou bash)
- ✅ Repositório clonado e com remoto configurado (ex.: origin → GitHub)
- ✅ Observação: comandos PowerShell usam pipeline e cmdlets; oferecemos alternativas em bash quando aplicável.

---

## 🚶 Passo a passo

> Os comandos a seguir foram testados. Use a variante adequada ao seu shell.

### 1️⃣ Remover branches locais que foram deletadas no remoto (sincronizar e podar)

Sincroniza com o remoto, remove referências de tracking obsoletas e apaga branches locais marcadas como [gone].

```powershell
git fetch -p; git branch -vv | Where-Object { $_ -match ": gone]" } | ForEach-Object { $_.Trim().Split(' ')[0] } | ForEach-Object { if ($_.Length -gt 0) { git branch -d $_ } }
```

Alternativa bash/zsh:

```bash
git fetch -p
git branch -vv | awk '/: gone]/{print $1}' | xargs -r -n 1 git branch -d
```

O que acontece:

- git fetch -p (ou --prune): remove referências remotas obsoletas.
- git branch -vv: lista branches com status de tracking; linhas com [: gone] indicam que a branch remota não existe mais.
- Remoção usa git branch -d (seguro, evita apagar branches com commits não mesclados).

---

### 2️⃣ Remover automaticamente branches que existem apenas localmente

Apaga todas as branches sem vínculo remoto e que não são a branch atual.

```powershell
git branch -vv | Where-Object { ($_ -notmatch '\[') -and ($_ -notmatch '\*') } | ForEach-Object { $_.Trim().Split(' ')[0] } | ForEach-Object { if ($_.Length -gt 0) { git branch -D $_ } }
```

Alternativa bash/zsh:

```bash
git branch -vv \
| awk '!/\[/ && !/^\*/ {print $1}' \
| xargs -r -n 1 git branch -D
```

Notas:

- Filtro sem [ indica ausência de tracking remoto.
- Exclusão usa -D (forçado), pois podem existir commits não enviados. Use com cautela.

---

### 3️⃣ Validar o resultado e revisar o estado

Listar branches restantes e verificar tracking:

```bash
git branch -vv
```

Dicas de revisão:

- Verifique se branches relevantes (ex.: main, develop, release/…) permanecem.
- Se algo importante foi removido, restaure via reflog (veja Troubleshooting).
- Opcional: remover localmente branches já mescladas em main/develop:

```bash
# Exemplo: remover branches totalmente mescladas em main
git checkout main
git pull --ff-only
git branch --merged | grep -vE '^\*|^(main|master|develop)$' | xargs -r -n 1 git branch -d
```

---

### 4️⃣ Opcional: configurar pruning automático e boas práticas

Ative prune no fetch para manter refs limpas:

```bash
# Em todos os repositórios do usuário
git config --global fetch.prune true

# Apenas neste repositório
git config fetch.prune true
```

Outras recomendações:

- Use nomes coerentes e efêmeros para branches de feature/bugfix.
- Faça merge ou rebase e crie PRs pequenos para reduzir branches “mortas”.
- Periodicamente rode git remote prune origin para limpar refs remotas:

```bash
git remote prune origin
```

---

## ⚠️ Armadilhas comuns

- ❗ Apagar a branch atual
  🔍 Causa: tentativa de deletar a branch em uso.
  🛠️ Solução: troque de branch antes (ex.: git checkout main) e repita o comando.

- ❗ Perder commits locais não enviados
  🔍 Causa: uso de -D em branch sem push.
  🛠️ Solução: prefira -d quando possível; entenda os riscos de -D. Use reflog para recuperar.

- ❗ Detached HEAD
  🔍 Causa: estar “preso” a um commit específico.
  🛠️ Solução: volte a uma branch nomeada (git checkout main) antes de limpar.

- ❗ Remoto diferente de origin
  🔍 Causa: comandos assumem origin como remoto padrão.
  🛠️ Solução: ajuste para o nome real do remoto (git remote -v; use-o nos comandos).

- ❗ Execução no PowerShell restrita
  🔍 Causa: política de execução bloqueando scripts/linhas avançadas.
  🛠️ Solução: execute no Windows Terminal com PowerShell atualizado ou use a alternativa bash (Git Bash).

---

## 🛠️ Troubleshooting (Erros Comuns)

- 💥 “error: The branch 'X' is not fully merged”
  → Causa: branch tem commits não integrados.
  → Ação: revise o diff; se tiver certeza, use -D. Caso contrário, faça merge/rebase antes.

- 🔎 Recuperar branch apagada por engano
  → Use o reflog para encontrar o último HEAD e recriar a branch:

  ```bash
  git reflog
  git checkout -b nome-branch RECENT_HEAD_HASH
  ```

- 🧭 Listar branches remotas e tracking

  ```bash
  git branch -r
  git branch -vv
  ```

- 🧹 Limpar referências remotas obsoletas manualmente

  ```bash
  git remote prune origin
  ```

- 🔄 Atualizar refs antes de decidir

  ```bash
  git fetch -p
  git branch -vv
  ```

- 🪪 “Permission denied” (scripts no Linux/macOS)
  → Causa: falta de permissão de execução.
  → Ação:
  ```bash
  chmod +x script.sh
  ```

---

## 📎 Referências

- 📘 Git fetch: https://git-scm.com/docs/git-fetch
- 📘 Git branch: https://git-scm.com/docs/git-branch
- 📘 Git remote prune: https://git-scm.com/docs/git-remote#Documentation/git-remote.txt-empruneem
- 📘 Git config: https://git-scm.com/docs/git-config

---

### ✔️ Dicas finais

- Repita a limpeza periodicamente para manter o repositório saudável.
- Prefira -d para exclusões seguras; use -D apenas quando tiver certeza.
- Ative fetch.prune para automatizar parte da manutenção.
