import sys
import uvicorn
from mcp.server.fastmcp import FastMCP
from tools.create_file import handle_create_file
from tools.get_weather import handle_get_weather
from starlette.middleware.cors import CORSMiddleware

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

mcp_app = mcp.sse_app()

class PureASGIRewriteMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            if scope["method"] == "POST" and scope["path"].endswith("/sse"):
                scope["path"] = "/messages"
        await self.app(scope, receive, send)

app_rewritten = PureASGIRewriteMiddleware(mcp_app)

app_with_cors = CORSMiddleware(
    app=app_rewritten,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("🚀 Arrancando Uvicorn con Interceptor ASGI y CORS para Copilot Studio...")
    
    uvicorn.run(
        app_with_cors, 
        host="0.0.0.0", 
        port=8000, 
        proxy_headers=True,
        forwarded_allow_ips="*"
    )