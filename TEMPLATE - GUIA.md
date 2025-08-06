# Guia Prático: {TÍTULO DO GUIA}

Atualizado em: YYYY-MM-DD • Versão: 1.0

## Sumário

- [Contexto/Objetivo](#contextoobjetivo)
- [Pré-requisitos](#pre-requisitos)
- [Passo a passo](#passo-a-passo)
  - [1) {Passo 1 — ação/objetivo}]#1-passo-1--acaoobjetivo)
  - [2) {Passo 2 — ação/objetivo}]#2-passo-2--acaoobjetivo)
  - [3) {Passo 3 — ação/objetivo}]#3-passo-3--acaoobjetivo)
  - [4) {Passo 4 — ação/objetivo}]#4-passo-4--acaoobjetivo)
- [Armadilhas comuns](#armadilhas-comuns)
- [Troubleshooting](#troubleshooting)
- [Referências](#referencias)

## Contexto/Objetivo

Explique claramente o problema que este guia resolve e o resultado esperado. Mantenha-o prático, objetivo e mensurável (o que o leitor terá ao final).

## Pré-requisitos

- Sistemas operacionais/versões suportadas
- Permissões necessárias (ex.: administrador, execução de scripts)
- Ferramentas e dependências (inclua links oficiais)
- Observações de compatibilidade (ex.: diferenças Windows/macOS/Linux)

## Passo a passo

Use comandos claros com explicações curtas. Prefira blocos de código com a linguagem definida. Inclua notas e dicas quando relevante.

### 1) {Passo 1 — ação/objetivo}

Breve descrição do que será feito e por quê.

```bash
# Exemplo (ajuste conforme o contexto do guia)
comando-1 --flag

# Alternativa (outro SO/ambiente)
comando-1-alternativo
```

Notas:

- Quando houver diferenças por SO, liste separadamente (Windows, macOS, Linux).
- Prefira caminhos sem espaços/caracteres especiais quando scripts falham.

### 2) {Passo 2 — ação/objetivo}

O que validar antes/depois, e como confirmar que deu certo.

```bash
# Comandos principais
comando-2 arg1 arg2

# Verificação
comando-2 --version
```

Dica: explique o critério de sucesso (ex.: saída esperada no terminal).

### 3) {Passo 3 — ação/objetivo}

Contexto do passo e impacto nos próximos.

```bash
# Exemplo de configuração/execução
comando-3 --enable-x --path "./exemplo"
```

### 4) {Passo 4 — ação/objetivo}

Quando aplicável, inclua exemplos e variações seguras.

```bash
# Execução/rodar serviço/script
comando-4 start

# Logs/estado
comando-4 status
```

## Armadilhas comuns

- Sintoma/erro: “Mensagem X …”
  Causa: motivo provável.
  Solução: ação objetiva com comando, quando possível.

- Conflito de versões/paths:
  Causa: misturar binários de ambientes diferentes.
  Solução: valide apontadores (which/where) e reative o ambiente correto.

- Caminhos com espaços/acentos:
  Causa: scripts de ativação ou parsing falham.
  Solução: use aspas ou prefira diretórios sem espaços.

Adapte os itens acima ao tema do guia com exemplos concretos.

## Troubleshooting

Sintoma → Causa provável → Ação recomendada.

- “Erro/stack Y …”
  → Causa: Z.
  → Ação: comando/checklist objetivo (ex.: “rode A; se falhar, verifique B; então aplique C”).

- “Comando não encontrado”
  → PATH não configurado ou ferramenta não instalada.
  → Reinstale/configure PATH e valide com `which/where`.

- “Permissão negada”
  → Falta de privilégios/execução de scripts bloqueada.
  → Ajuste permissões/política (ex.: `chmod +x` no Unix; `ExecutionPolicy` no PowerShell).

Inclua mensagens e correções frequentes específicas do tema do guia.

## Referências

- Documentação oficial 1: <URL>
- Guia/artigo confiável 2: <URL>
- Repositório/ferramenta 3: <URL>
