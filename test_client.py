import asyncio
import sys
import traceback
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

async def test_mcp():
    print("Iniciando cliente de prueba MCP...")

    server_url = "https://22fe-2800-40-39-2838-c4d8-c64f-cfe5-92e8.ngrok-free.app/"

    print(f"\n⏳ Conectando por Streamable HTTP a: {server_url}...")

    try:
        async with streamablehttp_client(server_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:

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
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(test_mcp())
    except KeyboardInterrupt:
        print("\nSaliendo...")