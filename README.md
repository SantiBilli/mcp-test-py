# Servidor MCP (Model Context Protocol) en Python

Este proyecto implementa un servidor Web que actúa como host bajo el **Model Context Protocol (MCP)** utilizando Python. Su objetivo es permitir a asistentes de inteligencia artificial (como Copilot u otros LLMs) descubrir e invocar herramientas personalizadas para interactuar con tu entorno local y servicios externos.

## 🛠️ Tecnologías Usadas y Por Qué

- **[Python](https://www.python.org/)**: Lenguaje principal del servidor, elegido por su simplicidad y gran ecosistema para integrar herramientas y APIs.
- **[Starlette](https://www.starlette.io/)**: Framework web ASGI ligero y de alto rendimiento. Se encarga de manejar las rutas HTTP (como `/`, `/sse`, `/messages`), recibir los payloads JSON de las peticiones del LLM y devolver las respuestas correspondientes.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor web ASGI ultrarrápido. Proporciona la infraestructura de red para ejecutar la aplicación web de Starlette, manteniéndola accesible en el puerto local (`8000`).
- **[uv](https://docs.astral.sh/uv/)**: Gestor de paquetes y entornos virtuales para Python extremadamente rápido (creado en Rust). Se utiliza en este proyecto para ejecutar los scripts (`uv run`) de manera eficiente, instalando dependencias al vuelo si es necesario y gestionando el entorno.

## ⚙️ Arquitectura y Herramientas (Tools)

El punto de entrada principal del servidor es `server.py`. Este archivo define un manejador genérico que procesa los mensajes del protocolo MCP (como `initialize`, `tools/list`, y `tools/call`). 

Las herramientas ejecutables (las acciones concretas que el asistente puede solicitar) están modularizadas dentro de la carpeta `tools/`. Actualmente se expone la siguiente:

1. 🌤️ **`get_weather`** (`tools/get_weather.py`)
   - **Descripción**: Consulta y devuelve el estado del clima actual en una ubicación específica.
   - **Parámetros requeridos**: `city` (nombre de la ciudad).

Cuando la IA decide utilizar alguna herramienta, envía una solicitud `tools/call`. El servidor identifica la herramienta solicitada e invoca de manera asíncrona la función correspondiente (`handle_get_weather`).

## 🚀 Cómo ejecutarlo

Para arrancar el servidor MCP localmente y dejarlo a la escucha de las peticiones (por defecto en `http://0.0.0.0:8000`):

```bash
uv run python server.py
```

Para probar la conexión (simulando peticiones de inicialización o llamadas a herramientas como si fueses un cliente MCP):

```bash
uv run python test_client.py
```
