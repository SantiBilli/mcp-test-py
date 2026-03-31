from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from models.blocks import CATALOGO_BLOQUES
from tools.onedrive import create_json_onedrive, delete_json_onedrive
from api.services import get_bots_list_json, get_bot_data_json
from handlers.chat import handle_chat


async def get_blocks_api(request: Request):
    return JSONResponse({"success": True, "bloques": CATALOGO_BLOQUES})


async def get_bots_api(request: Request):
    try:
        lista_bots = await get_bots_list_json()
        return JSONResponse({"success": True, "bots": lista_bots})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


async def create_bot_api(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"success": False, "error": "JSON inválido"}, status_code=400)

    filename = body.get("filename")
    if not filename:
        return JSONResponse(
            {"success": False, "error": "Se requiere 'filename'"},
            status_code=400,
        )

    try:
        result = await create_json_onedrive(filename)
        return JSONResponse({"success": True, "message": result})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


async def delete_bot_api(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"success": False, "error": "JSON inválido"}, status_code=400)

    filename = body.get("filename")
    if not filename:
        return JSONResponse(
            {"success": False, "error": "Se requiere 'filename'"},
            status_code=400,
        )

    try:
        result = await delete_json_onedrive(filename)
        return JSONResponse({"success": True, "message": result})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

async def get_bot_detail_api(request: Request):
    filename = request.path_params.get("filename")
    if not filename:
        return JSONResponse(
            {"success": False, "error": "Se requiere el nombre del bot"},
            status_code=400,
        )

    try:
        data = await get_bot_data_json(filename)
        if data is None:
            return JSONResponse(
                {"success": False, "error": f"El bot '{filename}' no existe"},
                status_code=404,
            )
        return JSONResponse({"success": True, "bot": data})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


api_routes = [
    Route("/api/blocks", endpoint=get_blocks_api, methods=["GET"]),
    Route("/api/bots", endpoint=get_bots_api, methods=["GET"]),
    Route("/api/bots/create", endpoint=create_bot_api, methods=["POST"]),
    Route("/api/bots/delete", endpoint=delete_bot_api, methods=["DELETE"]),
    Route("/api/bots/{filename}", endpoint=get_bot_detail_api, methods=["GET"]),
    Route("/api/chat", endpoint=handle_chat, methods=["POST"]),
]
