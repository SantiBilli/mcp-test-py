import sys
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
    port = 8000
    print(f"Servidor MCP HTTP arrancando vía FastMCP en el puerto {port}")
    print(f"Ejecuta en otra terminal: ngrok http {port}")
    
    mcp.run(transport="sse") 
