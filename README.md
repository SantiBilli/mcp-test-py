# MCP OneDrive Server

Servidor MCP (Model Context Protocol) escrito en Python que expone herramientas para manipular archivos JSON en OneDrive y consultar el clima. Puede ser consumido por cualquier cliente MCP compatible (ej: GitHub Copilot, Claude Desktop, etc).

## Tecnologías

| Tecnología        | Uso                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------ |
| **Python 3.11+**  | Lenguaje principal del servidor                                                      |
| **Starlette**     | Framework web ASGI que maneja las rutas HTTP                                         |
| **Uvicorn**       | Servidor ASGI que corre la aplicación                                                |
| **httpx**         | Cliente HTTP async para llamar APIs externas (Microsoft Graph, Open-Meteo)           |
| **python-dotenv** | Carga las variables de entorno desde el archivo `.env`                               |
| **msal**          | Librería de Microsoft para autenticación OAuth2 (usada en `sacar_token.py`)          |
| **mcp**           | SDK del protocolo MCP, se usa en el cliente de prueba y en los tipos (`TextContent`) |
| **uv**            | Gestor de paquetes y entornos virtuales (alternativa moderna a pip)                  |
| **Docker**        | Containerización para deploy                                                         |

## Estructura del proyecto

```
mcp-test-py/
│
├── server.py                    # Punto de entrada del servidor
├── handlers/
│   ├── __init__.py              # Marca la carpeta como paquete Python
│   └── mcp.py                   # Lógica del protocolo MCP (JSON-RPC)
├── tools/
│   ├── __init__.py              # Marca la carpeta como paquete Python
│   ├── registry.py              # Definiciones de las herramientas (schemas JSON)
│   ├── dispatcher.py            # Mapea el nombre de cada tool a su función
│   ├── get_weather.py           # Implementación de la tool de clima
│   └── onedrive.py              # Implementación de las tools de OneDrive
│
├── sacar_token.py               # Script auxiliar para obtener el refresh token de Microsoft
├── test_client.py               # Cliente de prueba que se conecta al servidor por SSE
│
├── .env                         # Variables de entorno (credenciales)
├── .gitignore                   # Archivos ignorados por Git
├── requirements.txt             # Dependencias (formato pip)
├── pyproject.toml               # Configuración del proyecto (formato uv/pip)
├── uv.lock                      # Lockfile generado por uv
└── Dockerfile                   # Imagen Docker para deploy
```

## Descripción de archivos

### `server.py`

Punto de entrada. Configura las rutas HTTP (`/`, `/sse`, `/messages`), aplica el middleware de CORS y arranca Uvicorn en el puerto 8000.

### `handlers/mcp.py`

Maneja los mensajes del protocolo MCP usando JSON-RPC 2.0. Responde a 4 métodos:

- **`initialize`** — Devuelve la versión del protocolo, las capacidades del servidor y su info.
- **`notifications/initialized`** — Confirmación de que el cliente se inicializó.
- **`tools/list`** — Devuelve la lista de herramientas disponibles (desde `registry.py`).
- **`tools/call`** — Ejecuta una herramienta específica (delegando a `dispatcher.py`).

### `tools/registry.py`

Lista centralizada con las definiciones de cada herramienta. Cada una tiene un `name`, `description` e `inputSchema` que describe sus parámetros. Si querés agregar una herramienta nueva, empezá definiendo su schema acá.

### `tools/dispatcher.py`

Recibe el nombre de una herramienta y sus argumentos, y delega la ejecución a la función correspondiente. Si querés agregar una herramienta nueva, sumá el mapeo acá.

### `tools/get_weather.py`

Herramienta que consulta el clima actual de una ciudad usando la API gratuita de [Open-Meteo](https://open-meteo.com/). Primero geocodifica la ciudad y luego consulta la temperatura y velocidad del viento.

### `tools/onedrive.py`

5 herramientas para manipular archivos JSON en OneDrive a través de la API de Microsoft Graph:

| Tool                   | Qué hace                                                       |
| ---------------------- | -------------------------------------------------------------- |
| `create_json_onedrive` | Crea un archivo JSON nuevo en la carpeta `AutoClickFiles/`     |
| `read_json_onedrive`   | Lee y devuelve el contenido de un archivo JSON                 |
| `modify_json_onedrive` | Modifica una propiedad dentro de un JSON existente             |
| `delete_json_onedrive` | Elimina un archivo JSON                                        |
| `rename_json_onedrive` | Renombra un archivo JSON y actualiza su campo `nombre` interno |

### `sacar_token.py`

Script que se corre **una sola vez** para obtener el `MICROSOFT_REFRESH_TOKEN`. Usa el flujo de autenticación por dispositivo (device flow) de Microsoft: te da un código, lo ingresás en el navegador, y te devuelve el refresh token.

### `test_client.py`

Cliente de prueba que se conecta al servidor por SSE, llama a `initialize` y `tools/list`, e imprime las herramientas disponibles. Útil para verificar que el servidor funciona correctamente.

### `Dockerfile`

Imagen Docker basada en `python:3.13-slim` con `uv` como gestor de paquetes. Expone el puerto 8000 y corre `server.py`.

## Credenciales (`.env`)

El archivo `.env` contiene 3 variables necesarias para conectarse a la API de Microsoft Graph (OneDrive):

```env
MICROSOFT_CLIENT_ID=tu_client_id
MICROSOFT_CLIENT_SECRET=tu_client_secret
MICROSOFT_REFRESH_TOKEN=tu_refresh_token
```

### ¿Cómo obtener las credenciales para otra cuenta?

1. **`MICROSOFT_CLIENT_ID`** y **`MICROSOFT_CLIENT_SECRET`**:
   - Andá a [Azure Portal > App registrations](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
   - Creá una nueva app (o usá una existente)
   - El **Client ID** está en la página principal de la app
   - El **Client Secret** se genera en **Certificates & secrets > New client secret**
   - En **API permissions** asegurate de tener el permiso `Files.ReadWrite`
   - En **Authentication** habilitá "Allow public client flows" (necesario para el device flow)

2. **`MICROSOFT_REFRESH_TOKEN`**:
   - Primero actualizá el `CLIENT_ID` en `sacar_token.py` con tu nuevo Client ID
   - Corré el script: `python sacar_token.py`
   - Seguí las instrucciones que aparecen en consola (ingresar un código en el navegador)
   - Copiá el refresh token que te devuelve y pegalo en el `.env`

> ⚠️ El refresh token puede expirar si no se usa por 90 días. Si eso pasa, volvé a correr `sacar_token.py`.

## Cómo correr

### Local

```bash
# Instalar dependencias
uv sync

# Correr el servidor
uv run python server.py
```

El servidor arranca en `http://localhost:8000`.

### Docker

```bash
docker build -t mcp-onedrive .
docker run -p 8000:8000 --env-file .env mcp-onedrive
```

### Probar la conexión

Con el servidor corriendo, en otra terminal:

```bash
uv run python test_client.py
```

## Cómo agregar una herramienta nueva

1. Creá la función en un archivo dentro de `tools/` (o en uno existente)
2. Agregá la definición del schema en `tools/registry.py`
3. Agregá el mapeo nombre → función en `tools/dispatcher.py`
