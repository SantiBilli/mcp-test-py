import sys
import os
from dotenv import load_dotenv

load_dotenv()

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from tools.get_weather import handle_get_weather

CLIENT_ID=os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET=os.getenv("MICROSOFT_CLIENT_SECRET")
REFRESH_TOKEN=os.getenv("MICROSOFT_REFRESH_TOKEN")

async def mcp_direct_handler(request: Request):
    try:
        payload = await request.json()
    except:
        return JSONResponse({"status": "ok"})

    method = payload.get("method")
    msg_id = payload.get("id")

    print(f"🤖 Copilot solicita: {method}")

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

    elif method == "notifications/initialized":
        return JSONResponse({"jsonrpc": "2.0"})

    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
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

    elif method == "tools/call":
        params = payload.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        print(f"⚙️ Ejecutando: {tool_name} con {args}")

        try:
            if tool_name == "get_weather":
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