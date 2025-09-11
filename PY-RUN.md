# PY-RUN.md: Python Application Runner Template

## Template

```python
#!/usr/bin/env python3
"""
Script para iniciar a aplicação FastAPI
"""

import uvicorn
import sys
from pathlib import Path

# Adicionar o diretório raiz ao Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings


def main():
    """Função principal para iniciar o servidor"""

    print("🚀 Iniciando API")
    print("📡 Servidor: http://0.0.0.0:8000")
    print("📖 Docs: http://0.0.0.0:8000/docs")
    print(f"🔧 Debug: {'ON' if settings.DEBUG_MODE else 'OFF'}")
    print("-" * 40)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG_MODE,
        log_level="info" if not settings.DEBUG_MODE else "debug",
    )


if __name__ == "__main__":
    main()
```

## How to Use

1. Create `run_api.py` in project root
2. Replace `app` with current project module name
3. Update port/host if needed
4. Run with `python run_api.py`
