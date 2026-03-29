import sys
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

# Importamos tus herramientas directamente
from tools.create_file import handle_create_file
from tools.get_weather import handle_get_weather

# --- EL TRADUCTOR NATIVO PARA COPILOT ---
async def mcp_direct_handler(request: Request):
    try:
        payload = await request.json()
    except:
        return JSONResponse({"status": "ok"})

    method = payload.get("method")
    msg_id = payload.get("id")

    print(f"🤖 Copilot solicita: {method}")

    # 1. Copilot saluda
    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "servidor-vps-santi", "version": "1.0.0"}
            }
        })

    # 2. Copilot confirma conexión
    elif method == "notifications/initialized":
        return JSONResponse({"jsonrpc": "2.0"})

    # 3. Copilot pide la lista de herramientas
    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "create_file",
                        "description": "Crea un archivo de texto en la computadora local",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "Ruta de la carpeta"},
                                "name": {"type": "string", "description": "Nombre del archivo"}
                            },
                            "required": ["path", "name"]
                        }
                    },
                    {
                        "name": "get_weather",
                        "description": "Obtiene el clima actual de una ciudad",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string", "description": "Nombre de la ciudad"}
                            },
                            "required": ["city"]
                        }
                    }
                ]
            }
        })

    # 4. Copilot ejecuta una herramienta
    elif method == "tools/call":
        params = payload.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        print(f"⚙️ Ejecutando: {tool_name} con {args}")

        try:
            if tool_name == "create_file":
                res = await handle_create_file(args.get("path"), args.get("name"))
                result_text = res[0].text
            elif tool_name == "get_weather":
                res = await handle_get_weather(args.get("city"))
                result_text = res[0].text
            else:
                result_text = f"Herramienta no encontrada."
        except Exception as e:
            result_text = f"Error: {str(e)}"

        return JSONResponse({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [{"type": "text", "text": result_text}]
            }
        })

    return JSONResponse({"jsonrpc": "2.0", "id": msg_id})

# Escuchamos en todas las rutas posibles por si Copilot se equivoca
app = Starlette(routes=[
    Route("/", endpoint=mcp_direct_handler, methods=["POST", "GET"]),
    Route("/sse", endpoint=mcp_direct_handler, methods=["POST", "GET"]),
    Route("/messages", endpoint=mcp_direct_handler, methods=["POST", "GET"])
])

app_with_cors = CORSMiddleware(
    app=app, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

if __name__ == "__main__":
    print("🚀 Arrancando Servidor MCP NATIVO (Cero dependencias) para Copilot...")
    uvicorn.run(app_with_cors, host="0.0.0.0", port=8000)