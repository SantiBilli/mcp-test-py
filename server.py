import uvicorn
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware

load_dotenv()

from handlers.mcp import mcp_handler
# from api.routes import api_routes

app = Starlette(
    routes=[
        Route("/", endpoint=mcp_handler, methods=["POST", "GET"]),
        Route("/sse", endpoint=mcp_handler, methods=["POST", "GET"]),
        Route("/messages", endpoint=mcp_handler, methods=["POST", "GET"]),

        # *api_routes,
    ]
)

app_with_cors = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("🚀 Arrancando MCP Server modularizado con OneDrive y Clima...")
    uvicorn.run(app_with_cors, host="0.0.0.0", port=8000)