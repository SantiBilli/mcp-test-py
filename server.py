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


mcp_app = mcp.sse_app()

if __name__ == "__main__":
    print("Arrancando Uvicorn nativo en 0.0.0.0:8000 (con soporte para Proxy en Coolify)...")
    
    uvicorn.run(
        mcp_app, 
        host="0.0.0.0", 
        port=8000, 
        proxy_headers=True,       
        forwarded_allow_ips="*"     
    )