import os
import uvicorn
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

load_dotenv()

from tools.onedrive import create_json_onedrive, modify_json_onedrive, delete_json_onedrive
from tools.get_weather import handle_get_weather

async def mcp_direct_handler(request: Request):
    try:
        payload = await request.json()
    except:
        return JSONResponse({"status": "ok"})

    method = payload.get("method")
    msg_id = payload.get("id")

    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mcp-onedrive", "version": "1.0.0"}
            }
        })

    elif method == "notifications/initialized":
        return JSONResponse({"jsonrpc": "2.0"})

    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0", "id": msg_id,
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
                    },
                    {
                        "name": "create_json_onedrive",
                        "description": "Crea un nuevo archivo JSON en la carpeta AutoClickFiles de OneDrive",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "filename": {"type": "string", "description": "Nombre del archivo (sin .json)"},
                                "initial_data": {"type": "object", "description": "Diccionario JSON con los datos iniciales"}
                            },
                            "required": ["filename", "initial_data"]
                        }
                    },
                    {
                        "name": "modify_json_onedrive",
                        "description": "Modifica o agrega un valor en un archivo JSON existente en AutoClickFiles",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "filename": {"type": "string", "description": "Nombre del archivo (sin .json)"},
                                "key": {"type": "string", "description": "La llave o propiedad a modificar"},
                                "value": {"type": "string", "description": "El nuevo valor"}
                            },
                            "required": ["filename", "key", "value"]
                        }
                    },
                    {
                        "name": "delete_json_onedrive",
                        "description": "Elimina un archivo JSON de la carpeta AutoClickFiles en OneDrive",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "filename": {"type": "string", "description": "Nombre del archivo (sin .json)"}
                            },
                            "required": ["filename"]
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
            elif tool_name == "create_json_onedrive":
                result_text = await create_json_onedrive(args.get("filename"), args.get("initial_data"))
            elif tool_name == "modify_json_onedrive":
                result_text = await modify_json_onedrive(args.get("filename"), args.get("key"), str(args.get("value")))
            elif tool_name == "delete_json_onedrive":
                result_text = await delete_json_onedrive(args.get("filename"))
            else:
                result_text = f"Herramienta {tool_name} no encontrada."
        except Exception as e:
            result_text = f"Error del servidor: {str(e)}"

        return JSONResponse({
            "jsonrpc": "2.0", "id": msg_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        })

    return JSONResponse({"jsonrpc": "2.0", "id": msg_id})

app = Starlette(routes=[
    Route("/", endpoint=mcp_direct_handler, methods=["POST", "GET"]),
    Route("/sse", endpoint=mcp_direct_handler, methods=["POST", "GET"]),
    Route("/messages", endpoint=mcp_direct_handler, methods=["POST", "GET"])
])

app_with_cors = CORSMiddleware(app=app, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    print("🚀 Arrancando MCP Server modularizado con OneDrive y Clima...")
    uvicorn.run(app_with_cors, host="0.0.0.0", port=8000)