from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from models.blocks import CATALOGO_BLOQUES
from tools.onedrive import get_bots_list_json
from handlers.chat import handle_chat


async def get_blocks_api(request: Request):
    return JSONResponse({"success": True, "bloques": CATALOGO_BLOQUES})


async def get_bots_api(request: Request):
    try:
        lista_bots = await get_bots_list_json()
        return JSONResponse({"success": True, "bots": lista_bots})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


api_routes = [
    Route("/api/blocks", endpoint=get_blocks_api, methods=["GET"]),
    Route("/api/bots", endpoint=get_bots_api, methods=["GET"]),
    Route("/api/chat", endpoint=handle_chat, methods=["POST"]),
]
