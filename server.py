import sys
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import create_mcp_server
from tools.create_file import handle_create_file
from tools.get_weather import handle_get_weather

# Creamos el servidor base
mcp = FastMCP("mcp-server")

@mcp.tool()
async def create_file(path: str, name: str) -> str:
    print(f"📝 Copilot quiere crear '{name}' en '{path}'")
    return (await handle_create_file(path, name))[0].text

@mcp.tool()
async def get_weather(city: str) -> str:
    print(f"🌍 Copilot está consultando el clima para: {city}")
    return (await handle_get_weather(city))[0].text

# --- LA MAGIA: Extraemos el manejador HTTP estándar ---
# Copilot Studio utiliza HTTP puro, no SSE.
mcp_server = mcp._mcp_server
mcp_server.request_handler = create_mcp_server(mcp)

async def handle_mcp_request(request):
    # Recibe el POST de Copilot y se lo pasa directo al manejador interno
    response = await mcp_server.request_handler(
        await request.body(), 
        request.headers
    )
    return response

# Creamos una aplicación simple que escuche en /messages (o en la raíz)
app = Starlette(routes=[
    Route("/", endpoint=handle_mcp_request, methods=["POST"]),
    Route("/messages", endpoint=handle_mcp_request, methods=["POST"])
])

# Agregamos el CORS
app_with_cors = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("🚀 Arrancando servidor MCP sobre HTTP estándar para Copilot Studio...")
    uvicorn.run(app_with_cors, host="0.0.0.0", port=8000)