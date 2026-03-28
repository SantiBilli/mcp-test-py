import asyncio
import sys
import traceback  # <-- Importación agregada para desglosar el error
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def test_mcp():
    print("Iniciando cliente de prueba MCP...")

    # base_url = "https://methodology-usb-facility-offline.trycloudflare.com"
    # base_url = "http://localhost:8000"
    base_url = "https://fbe8-170-239-171-159.ngrok-free.app"
        
    baseUrl = base_url.rstrip('/')
    sse_url = f"{baseUrl}/sse"
    
    print(f"\n⏳ Conectando por SSE a: {sse_url}...")
    
    try:
        async with sse_client(sse_url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                
                await session.initialize()
                print("✅ ¡Conectado exitosamente al servidor MCP!\n")
                
                print("🔎 Consultando herramientas configuradas en el servidor...")
                tools_response = await session.list_tools()
                
                if not tools_response.tools:
                    print("No se encontraron herramientas (tools=[]).")
                else:
                    print(f"\n🛠️ Se encontraron {len(tools_response.tools)} herramientas:")
                    for t in tools_response.tools:
                        desc = t.description if t.description else "Sin descripción"
                        print(f"  - {t.name}: {desc}")
                
                print("\n💡 El servidor responde correctamente. Saliendo...")
                
    except Exception as err:
        print("\n❌ Error de conexión conectando al servidor. Detalle técnico:", file=sys.stderr)
        # Esto imprimirá la traza completa (traceback) en lugar de solo "TaskGroup (1 sub-exception)"
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(test_mcp())
    except KeyboardInterrupt:
        print("\nSaliendo...")