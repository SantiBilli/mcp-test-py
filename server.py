import sys
import os
import json
import httpx
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

# --- CREDENCIALES DESDE COOLIFY ---
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("MICROSOFT_REFRESH_TOKEN")

# --- LÓGICA DE ONEDRIVE ---
async def get_access_token():
    """Usa tu Refresh Token eterno para conseguir un pase temporal de 60 minutos"""
    url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, data=data)
        res.raise_for_status()
        return res.json()["access_token"]

async def create_json_onedrive(filename: str, initial_data: dict) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        res = await client.put(url, headers=headers, content=json.dumps(initial_data, indent=4))
        res.raise_for_status()
    return f"✅ Archivo {filename}.json creado exitosamente en tu carpeta AutoClickFiles de OneDrive."

async def modify_json_onedrive(filename: str, key: str, value: str) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        # 1. Descargar el archivo actual
        get_res = await client.get(url, headers=headers)
        if get_res.status_code == 404:
            return f"❌ Error: El archivo {filename}.json no existe en OneDrive."
        get_res.raise_for_status()
        data = get_res.json()
        
        # 2. Modificar el dato
        data[key] = value
        
        # 3. Volver a subirlo
        headers["Content-Type"] = "application/json"
        put_res = await client.put(url, headers=headers, content=json.dumps(data, indent=4))
        put_res.raise_for_status()
    return f"✅ Archivo {filename}.json modificado. Clave '{key}' actualizada a '{value}'."

async def delete_json_onedrive(filename: str) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        res = await client.delete(url, headers=headers)
        if res.status_code == 404:
            return f"❌ Error: El archivo {filename}.json no existe."
        res.raise_for_status()
    return f"🗑️ Archivo {filename}.json eliminado correctamente de OneDrive."

# --- EL TRADUCTOR NATIVO PARA COPILOT ---
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
            if tool_name == "create_json_onedrive":
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
    print("🚀 Arrancando MCP Server integrado con OneDrive...")
    uvicorn.run(app_with_cors, host="0.0.0.0", port=8000)