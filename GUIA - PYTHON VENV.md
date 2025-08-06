# Guia Prático: Ambientes Virtuais Python (venv) e Requirements

Atualizado em: 2025-08-06 • Versão: 1.0

Sumário

- [Contexto/Objetivo](#contextoobjetivo)
- [Pré-requisitos](#pré-requisitos)
- [Passo a passo](#passo-a-passo)
- [Armadilhas comuns](#armadilhas-comuns)
- [Troubleshooting](#troubleshooting)
- [Referências](#referências)

## Contexto/Objetivo

Este guia ensina, de forma prática, como criar e administrar ambientes virtuais Python (venv), ativá-los/desativá-los, atualizar `pip`, instalar e congelar dependências, e manter o arquivo `requirements.txt` atualizado. Serve para Windows, macOS e Linux, garantindo isolamento de dependências e reprodutibilidade.

## Pré-requisitos

- Python 3.8+ instalado
  - Windows: https://www.python.org/downloads/ ou Microsoft Store
  - macOS/Linux: geralmente há `python3`; se não, use o gerenciador de pacotes
- `pip` (vem com Python 3.4+)
- Permissões básicas de execução de scripts
  - PowerShell pode exigir ajuste de `ExecutionPolicy` (ver Armadilhas)
- Terminal:
  - Windows: PowerShell ou CMD
  - macOS/Linux: bash/zsh
- Opcional: `pyenv` (Linux/macOS) para múltiplas versões do Python

## Passo a passo

### 1) Verificar versões do Python e pip

```bash
# Windows (PowerShell/CMD)
py --version
py -m pip --version

# Alternativas (conforme sua instalação)
python --version
python -m pip --version

# macOS/Linux
python3 --version
python3 -m pip --version
```

Notas:

- Em Windows, prefira `py` (Python Launcher).
- Em macOS/Linux, prefira `python3`.

### 2) Criar o ambiente virtual (venv)

Escolha um nome (recomendado `.venv` ou `venv`):

```bash
# Windows (PowerShell/CMD)
py -m venv .venv

# macOS/Linux
python3 -m venv .venv
```

Isso criará a pasta `.venv` com um Python isolado.

### 3) Ativar o ambiente virtual

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat

# Windows Git Bash
source .venv/Scripts/activate

# macOS/Linux (bash/zsh)
source .venv/bin/activate
```

Dica: Após ativar, o prompt exibirá `(.venv)`.

### 4) Desativar o ambiente virtual

```bash
deactivate
```

### 5) Atualizar pip (dentro do venv ativo)

```bash
python -m pip install --upgrade pip
python -m pip --version
```

### 6) Instalar dependências do projeto

```bash
# Se houver requirements.txt
python -m pip install -r requirements.txt
```

Dica: inclua esse comando no README para facilitar onboarding.

### 7) Adicionar/atualizar dependências e congelar

```bash
# Exemplo de instalação
python -m pip install requests==2.32.3
python -m pip install "fastapi>=0.111,<0.112"

# Congelar o estado atual para reprodutibilidade
python -m pip freeze > requirements.txt
```

Importante: gere `requirements.txt` a partir de um venv limpo, contendo apenas o que o projeto usa.

### 8) Atualizar requirements para últimas versões compatíveis

Abordagem segura:

```bash
# Ajuste manualmente intervalos (ex.: >=, <) e reinstale
python -m pip install -r requirements.txt

# Opcional: usar pip-tools para resolver versões
python -m pip install pip-tools
pip-compile --upgrade  # gera/atualiza requirements.txt a partir de requirements.in
```

### 9) Verificar se pip/python apontam para o venv

```bash
# macOS/Linux
which python
which pip

# Windows
where python
where pip
```

Os caminhos devem apontar para `.venv` (ou `venv`). Se apontarem para o sistema, o venv não está ativo ou há conflito no PATH.

### 10) Rodar scripts/comandos no venv

```bash
python app.py
uvicorn main:app --reload
pytest
ruff check .
```

Sempre com o venv ativo para garantir as dependências corretas.

### 11) Remover/recriar o venv (quando necessário)

```bash
# 1) Apague a pasta do venv (ex.: .venv)
# 2) Recrie
python -m venv .venv      # macOS/Linux
# ou
py -m venv .venv          # Windows

# 3) Ative e reinstale dependências
source .venv/bin/activate # macOS/Linux
# ou
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
python -m pip install -r requirements.txt
```

## Armadilhas comuns

- PowerShell bloqueando ativação
  Sintoma: “Activate.ps1 is not digitally signed…”
  Causa: `ExecutionPolicy` restritiva.
  Solução (PowerShell como Administrador):

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```

  Depois: `.\.venv\Scripts\Activate.ps1`

- Misturar pip do sistema com o do venv
  Sintoma: pacotes “somem” ao rodar o app.
  Causa: instalou com pip global, executa com python do venv (ou vice-versa).
  Solução: ative o venv e use sempre `python -m pip …`.

- Caminhos com espaços ou acentuação
  Causa: scripts de ativação podem falhar.
  Solução: prefira caminhos sem espaços/caracteres especiais ou use aspas.

- `requirements.txt` desatualizado
  Sintoma: reprodutibilidade falha em outro PC/CI.
  Solução: sempre `pip freeze > requirements.txt` após alterações.

- `python` vs `py` vs `python3`
  Causa: aliases diferentes por SO/instalação.
  Solução: no Windows use `py`; em macOS/Linux use `python3`.

- Várias versões do Python instaladas
  Sintoma: venv criado com versão inesperada.
  Solução: especifique explicitamente a versão:
  - Windows: `py -3.11 -m venv .venv`
  - macOS/Linux: `python3.11 -m venv .venv`

## Troubleshooting

Sintoma → Causa provável → Ação recomendada.

- “pip: command not found” (macOS/Linux)
  → PATH aponta para Python antigo/ausente.
  → Use `python3 -m pip …` ou reinstale Python 3 e garanta que `python3` exista.

- “Activate.ps1 is not digitally signed” (Windows PowerShell)
  → `ExecutionPolicy` bloqueia scripts.
  → Rode `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e reative o venv.

- “ModuleNotFoundError: No module named 'X'”
  → Pacote não instalado no venv ativo.
  → Ative o venv e instale: `python -m pip install X`.

- “Permission denied” ao ativar (macOS/Linux)
  → Script sem permissão de execução.
  → `chmod +x .venv/bin/activate` e depois `source .venv/bin/activate`.

- “Using pip from (…/site-packages) outside venv”
  → PATH aponta para pip global.
  → Ative o venv; confirme com `which/where pip`.

- “venv criado com versão errada do Python”
  → `python`/`py` apontando para versão diferente.
  → Especifique a versão (ver Armadilhas).

- Problemas de SSL/certificados no macOS ao instalar pacotes
  → Certificados ausentes nas instalações do Python.org.
  → Execute o script “Install Certificates.command” que acompanha a instalação do Python no macOS.

## Referências

- venv (docs Python): https://docs.python.org/3/library/venv.html
- pip (docs): https://pip.pypa.io/en/stable/
- pyenv (gerenciar versões, macOS/Linux): https://github.com/pyenv/pyenv
- virtualenv: https://virtualenv.pypa.io/en/latest/
- pip-tools: https://github.com/jazzband/pip-tools
