import sys
import uvicorn
from mcp.server.fastmcp import FastMCP
from tools.create_file import handle_create_file
from tools.get_weather import handle_get_weather
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

mcp = FastMCP("mcp-server")

@mcp.tool()
async def create_file(path: str, name: str) -> str:
    return (await handle_create_file(path, name))[0].text

@mcp.tool()
async def get_weather(city: str) -> str:
    return (await handle_get_weather(city))[0].text

mcp_app = mcp.sse_app()

# --- EL MICRÓFONO OCULTO (Diagnóstico) ---
# Atrapamos el POST de Copilot para leer qué está enviando
async def diagnostic_post(request: Request):
    try:
        body = await request.body()
        payload = body.decode('utf-8')
        print("\n" + "="*50)
        print(f"🚨 [DIAGNÓSTICO] Copilot atacó la ruta: {request.url.path}")
        print(f"📦 [PAYLOAD RECIBIDO]:\n{payload}")
        print("="*50 + "\n")
        
        # Le respondemos en su mismo idioma para que no explote
        return JSONResponse([{"jsonrpc": "2.0", "result": {"tools": []}, "id": 1}])
    except Exception as e:
        print(f"❌ Error leyendo payload: {e}")
        return JSONResponse({"error": "ok"})

# Le ponemos la trampa tanto a la ruta /sse como a la ruta raíz
mcp_app.add_route("/sse", diagnostic_post, methods=["POST"])
mcp_app.add_route("/", diagnostic_post, methods=["POST"])
# ------------------------------------------

app_with_cors = CORSMiddleware(
    app=mcp_app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("🚀 Arrancando Uvicorn con Micrófono Oculto para Copilot...")
    uvicorn.run(app_with_cors, host="0.0.0.0", port=8000, proxy_headers=True, forwarded_allow_ips="*")