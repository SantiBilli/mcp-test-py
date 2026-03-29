import sys
import uvicorn
from mcp.server.fastmcp import FastMCP
from tools.create_file import handle_create_file
from tools.get_weather import handle_get_weather
from starlette.middleware.cors import CORSMiddleware  # <-- Importamos el portero CORS

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

# 2. Le ponemos el "portero" CORS para que apruebe las peticiones de Microsoft
app_with_cors = CORSMiddleware(
    app=mcp_app,
    allow_origins=["*"],          # Permite conexiones desde cualquier página (incluido Copilot)
    allow_credentials=True,
    allow_methods=["*"],          # Permite GET, POST, OPTIONS, etc.
    allow_headers=["*"],          # Permite cualquier cabecera
)

if __name__ == "__main__":
    print("🚀 Arrancando Uvicorn nativo en 0.0.0.0:8000 con CORS y Proxy...")
    
    # 3. Corremos la aplicación ya envuelta con CORS
    uvicorn.run(
        app_with_cors, 
        host="0.0.0.0", 
        port=8000, 
        proxy_headers=True,
        forwarded_allow_ips="*"
    )