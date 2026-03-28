import sys
import uvicorn
from mcp.server.fastmcp import FastMCP
from tools.create_file import handle_create_file
from tools.get_weather import handle_get_weather

mcp = FastMCP("mcp-server")

@mcp.tool()
async def create_file(path: str, name: str) -> str:
    results = await handle_create_file(path, name)
    return results[0].text

@mcp.tool()
async def get_weather(city: str) -> str:
    results = await handle_get_weather(city)
    return results[0].text

if __name__ == "__main__":
    print("Forzando a Uvicorn a abrir el puerto 0.0.0.0...")
    
    # --- LA TRAMPA: Interceptamos Uvicorn para forzar la IP y el puerto ---
    original_run = uvicorn.run
    def custom_run(*args, **kwargs):
        kwargs['host'] = "0.0.0.0"
        kwargs['port'] = 8000
        return original_run(*args, **kwargs)
    uvicorn.run = custom_run
    # ----------------------------------------------------------------------
    
    mcp.run(transport="sse")