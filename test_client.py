import sys
import uvicorn
from mcp.server.fastmcp import FastMCP
from tools.create_file import handle_create_file
from tools.get_weather import handle_get_weather
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware # <-- Importamos el interceptor

mcp = FastMCP("mcp-server")

@mcp.tool()
async def create_file(path: str, name: str) -> str:
    print(f"📝 [LOG HERRAMIENTA] Copilot quiere crear el archivo '{name}' en '{path}'")
    results = await handle_create_file(path, name)
    print(f"✅ [LOG HERRAMIENTA] Archivo '{name}' creado con éxito.")
    return results[0].text

@mcp.tool()
async def get_weather(city: str) -> str:
    print(f"🌍 [LOG HERRAMIENTA] Copilot está consultando el clima para: {city}")
    results = await handle_get_weather(city)
    return results[0].text

# 1. Extraemos la aplicación web nativa
mcp_app = mcp.sse_app()

# --- EL TRUCO PARA DOMAR A COPILOT STUDIO ---
class CopilotRewriteMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Si Copilot intenta hacer un POST a la ruta /sse, lo redirigimos a /messages
        if request.method == "POST" and request.url.path.endswith("/sse"):
            request.scope["path"] = "/messages"
        return await call_next(request)

mcp_app.add_middleware(CopilotRewriteMiddleware)
# --------------------------------------------

# 2. Le ponemos el "portero" CORS
app_with_cors = CORSMiddleware(
    app=mcp_app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("🚀 Arrancando Uvicorn nativo con adaptador para Copilot Studio...")
    
    uvicorn.run(
        app_with_cors, 
        host="0.0.0.0", 
        port=8000, 
        proxy_headers=True,
        forwarded_allow_ips="*"
    )