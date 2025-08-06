# 🛠️ Guia Prático: **{TÍTULO DO GUIA}**

📅 Atualizado em: `YYYY-MM-DD` • 🔖 Versão: `1.0`

---

## 📚 Sumário

- [🎯 Contexto e Objetivo](#contexto-e-objetivo)
- [✅ Pré-requisitos](#pré-requisitos)
- [🚶 Passo a passo](#passo-a-passo)
  - [1️⃣ {Passo 1 — ação/objetivo}](#1️⃣-passo-1--açãoobjetivo)
  - [2️⃣ {Passo 2 — ação/objetivo}](#2️⃣-passo-2--açãoobjetivo)
  - [3️⃣ {Passo 3 — ação/objetivo}](#3️⃣-passo-3--açãoobjetivo)
  - [4️⃣ {Passo 4 — ação/objetivo}](#4️⃣-passo-4--açãoobjetivo)
- [⚠️ Armadilhas comuns](#armadilhas-comuns)
- [🛠️ Troubleshooting (Erros Comuns)](#troubleshooting-erros-comuns)
- [📎 Referências](#referências)

---

## 🎯 Contexto e Objetivo

> Descreva brevemente:
>
> - O problema que este guia resolve.
> - O resultado final esperado.
> - Para quem o guia é útil.
>
> Seja direto e mensurável: o que o leitor terá feito ao final?

---

## ✅ Pré-requisitos

Liste tudo que o leitor precisa **antes de iniciar**:

- ✅ Sistemas operacionais suportados (ex.: Windows 10+, macOS 12+, Linux Ubuntu 20.04+)
- ✅ Permissões necessárias (ex.: administrador, sudo, execuções liberadas)
- ✅ Ferramentas e dependências (ex.: Git, Node.js) com links oficiais
- ✅ Observações importantes de compatibilidade entre plataformas

---

## 🚶 Passo a passo

> Use comandos **testados** com explicações claras.
> Evite jargões e prefira formatos práticos.
> Para comandos, use blocos com a linguagem definida (ex.: `bash`, `powershell`, etc).

### 1️⃣ {Passo 1 — ação/objetivo}

Descreva o **propósito** deste passo e o que será feito.

```bash
# Exemplo: Instalar a ferramenta principal
comando-1 --instalar

# Alternativa para Windows
comando-1.exe /install
```

📝 **Notas**:

- Se houver variações por sistema operacional, separe em subitens.
- Evite caminhos com espaços ou acentuação.

---

### 2️⃣ {Passo 2 — ação/objetivo}

Explique o que validar **antes e depois** deste passo.

```bash
# Executar o comando principal
comando-2 --iniciar

# Verificar a versão instalada
comando-2 --version
```

✔️ Critério de sucesso: explique o que o usuário deve ver.

---

### 3️⃣ {Passo 3 — ação/objetivo}

Contextualize o passo e seu impacto nos próximos.

```bash
# Exemplo de configuração
comando-3 --config "./caminho/config.json"
```

💡 Dica: se há parâmetros comuns ou recomendados, destaque-os aqui.

---

### 4️⃣ {Passo 4 — ação/objetivo}

Mostre como executar, testar ou finalizar a operação.

```bash
# Iniciar serviço/script
comando-4 start

# Verificar logs
comando-4 logs
```

📌 **Variações**:

- Exemplo 1: modo interativo
- Exemplo 2: execução em background

---

## ⚠️ Armadilhas comuns

Liste erros comuns com causa e solução. Foque nos pontos que mais geram dúvida.

- ❗ **Erro**: `Mensagem de erro X...`
  🔍 Causa: biblioteca ausente ou variável de ambiente mal configurada.
  🛠️ Solução: `export VAR=valor`, ou reinstale dependência.

- ❗ **Caminhos com espaços/acentos**
  🔍 Causa: scripts de parsing que não interpretam corretamente.
  🛠️ Solução: use aspas duplas ou prefira diretórios simples (`/meus/projetos/sem-acentos/`)

- ❗ **Conflito de versões**
  🔍 Causa: múltiplas versões da mesma ferramenta.
  🛠️ Solução: use `which`/`where` para validar o binário ativo.

---

## 🛠️ Troubleshooting (Erros Comuns)

Estruture os problemas com um formato lógico e direto.

- 💥 **“Erro: comando não encontrado”**
  → **Causa**: PATH não configurado corretamente
  → **Ação recomendada**:

  ```bash
  which nome-do-comando
  # ou
  echo $PATH
  ```

- 🔐 **“Permissão negada”**
  → **Causa**: falta de permissões de execução
  → **Ação**:

  ```bash
  chmod +x script.sh
  ```

- 📛 **“Stack trace com Exception Y…”**
  → **Causa provável**: má configuração inicial
  → **Solução**: revise os arquivos de configuração e rode:

  ```bash
  comando --config-check
  ```

Adicione erros específicos com soluções testadas conforme o tema do guia.

---

## 📎 Referências

- 📘 Documentação oficial: [https://exemplo.com/docs](https://exemplo.com/docs)
- 📰 Artigo complementar: [https://exemplo.com/blog](https://exemplo.com/blog)
- 💻 Repositório relacionado: [https://github.com/exemplo/projeto](https://github.com/exemplo/projeto)

---

### ✔️ Dicas finais

- Use este template como base para todos os guias.
- Mantenha consistência nos títulos, termos e estilo.
- Prefira comandos simples, exemplos reais e explicações úteis.

---
