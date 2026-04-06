from starlette.requests import Request
from starlette.responses import JSONResponse

from tools.registry import TOOL_DEFINITIONS
from tools.dispatcher import dispatch_tool

SERVER_INFO = {
    "name": "mcp-onedrive",
    "version": "1.0.0",
}

PROTOCOL_VERSION = "2024-11-05"


def _jsonrpc_response(msg_id, result: dict) -> JSONResponse:
    return JSONResponse({"jsonrpc": "2.0", "id": msg_id, "result": result})


async def mcp_handler(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"status": "ok"})

    method = payload.get("method")
    msg_id = payload.get("id")

    if method == "initialize":
        return _jsonrpc_response(msg_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        })

    if method == "notifications/initialized":
        return JSONResponse({"jsonrpc": "2.0"})

    if method == "tools/list":
        return _jsonrpc_response(msg_id, {"tools": TOOL_DEFINITIONS})

    if method == "tools/call":
        params = payload.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            user_token = auth_header.replace("Bearer ", "").strip()
            args["user_token"] = user_token
        else:
            return _jsonrpc_response(msg_id, {
                "content": [{"type": "text", "text": "❌ Acceso Denegado: Copilot no envió el token de seguridad corporativo en las cabeceras."}],
            })

        print(f"⚙️ Ejecutando: {tool_name} con {args}")

        try:
            result_text = await dispatch_tool(tool_name, args)
        except Exception as e:
            result_text = f"Error del servidor: {str(e)}"

        return _jsonrpc_response(msg_id, {
            "content": [{"type": "text", "text": result_text}],
        })

    return JSONResponse({"jsonrpc": "2.0", "id": msg_id})