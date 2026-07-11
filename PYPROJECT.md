# pyproject.toml — guia rápido

Referência para quem está habituado com `requirements.txt`: o que o `pyproject.toml`
faz neste projeto e como gerenciar/atualizar as dependências.

## pyproject.toml vs requirements.txt

O bloco `dependencies = [...]` do `pyproject.toml` é o equivalente direto do
`requirements.txt` — uma lista de pacotes com restrições de versão. A diferença é
que o `pyproject.toml` (padrão oficial moderno, PEP 621) descreve o projeto inteiro
num arquivo só:

| | `requirements.txt` | `pyproject.toml` |
|---|---|---|
| Dependências | lista solta | `[project].dependencies` |
| Versão do Python | não declara | `requires-python = ">=3.12"` |
| Metadados (nome, versão) | não tem | `[project]` |
| Como empacotar | não tem | `[build-system]` (aqui: hatchling, empacota `app/`) |
| Instalação | `pip install -r requirements.txt` | `pip install -e .` |
| Versões | costuma travar (`==`) | declara intervalos (`>=`); travamento fica num lock file separado |

Este projeto **não tem lock file** — na prática o comportamento é o de um
requirements com `>=`.

## Setup inicial

```powershell
cd api
python -m venv .venv
.venv\Scripts\python -m pip install -e .
copy .env.example .env   # preencher BRIGHTDATA_API_KEY no mínimo
```

O `-e .` instala o projeto em modo editável: o pip lê as dependências do
`pyproject.toml` e as resolve. Depois é só rodar `run-server.bat`.

## Adicionar uma dependência

Edite a lista `dependencies` no `pyproject.toml` e reinstale:

```powershell
.venv\Scripts\python -m pip install -e .
```

## Atualizar pacotes

Como as restrições usam `>=`, atualizar é reinstalar pedindo upgrade:

```powershell
# Ver o que está desatualizado antes de mexer
.venv\Scripts\python -m pip list --outdated

# Atualizar tudo que está em dependencies
.venv\Scripts\python -m pip install -e . --upgrade

# Atualizar só um pacote específico
.venv\Scripts\python -m pip install --upgrade fastapi

# Ver a versão instalada de algo
.venv\Scripts\python -m pip show pydantic-ai
```

### Cuidados

1. **Major versions:** `>=` sem teto pode puxar uma major nova com breaking
   changes. O `pydantic-ai` é o mais arriscado (versão 0.x, muda rápido). Depois
   de atualizar, rode o servidor e teste o `POST /import/airbnb`. Se algo quebrar,
   trave o pacote no `pyproject.toml` (ex.: `pydantic-ai>=0.0.14,<0.1`) e
   reinstale.

2. **Reprodutibilidade:** sem lock file, o build do Dockerfile resolve as versões
   na hora — pode divergir do ambiente local. Se isso virar problema, migrar para
   o [uv](https://docs.astral.sh/uv/): `uv sync` gera um `uv.lock` e
   `uv lock --upgrade` faz o update controlado. Para o estágio atual, pip puro
   resolve.
