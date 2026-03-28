FROM python:3.13-slim

# Copiamos uv directamente desde su imagen oficial (extremadamente rápido)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Forzamos a que Python imprima los logs en tiempo real en la consola de Coolify
ENV PYTHONUNBUFFERED=1
# Le decimos a FastMCP que escuche en todas las interfaces de red y en el puerto 8000
ENV HOST=0.0.0.0
ENV PORT=8000

# Copiamos los archivos de configuración de dependencias primero
COPY pyproject.toml uv.lock* requirements.txt* ./

# Instalamos las dependencias según el gestor que estés usando
RUN if [ -f "pyproject.toml" ]; then uv sync --system --no-dev; \
    elif [ -f "requirements.txt" ]; then uv pip install --system -r requirements.txt; \
    else uv pip install --system mcp; fi

# Copiamos el resto del código fuente (server.py y la carpeta tools)
COPY . .

EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "server.py"]