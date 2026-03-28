FROM python:3.13-slim

# Copiamos uv directamente desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Copiamos los archivos de configuración
COPY pyproject.toml uv.lock* requirements.txt* ./

# Quitamos el '--system' de uv sync para que cree un entorno virtual (.venv) por defecto
RUN if [ -f "pyproject.toml" ]; then uv sync --no-dev; \
    elif [ -f "requirements.txt" ]; then uv venv && uv pip install -r requirements.txt; \
    else uv venv && uv pip install mcp; fi

COPY . .

EXPOSE 8000

# Cambiamos el comando final para usar 'uv run', que automáticamente detectará el .venv
CMD ["uv", "run", "python", "server.py"]