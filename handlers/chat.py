"""
Handler de chat que conecta el frontend con Claude API.
Claude recibe las herramientas MCP y puede ejecutarlas via dispatch_tool().
"""

import os
import anthropic
from starlette.requests import Request
from starlette.responses import JSONResponse

from tools.registry import TOOL_DEFINITIONS
from tools.dispatcher import dispatch_tool


ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
MAX_TOOL_ROUNDS = 10
SYSTEM_PROMPT = """Sos un asistente inteligente que ayuda a gestionar bots de automatización.
Tenés acceso a herramientas para crear, leer, modificar y eliminar bots guardados en OneDrive,
y también podés consultar el clima. Respondé siempre en español de forma concisa y amigable."""


def _convert_tools_for_claude(mcp_tools: list) -> list:
    """
    Convierte TOOL_DEFINITIONS (formato MCP) al formato que espera Claude API.
    MCP:   { name, description, inputSchema: { type, properties, required } }
    Claude: { name, description, input_schema: { type, properties, required } }
    """
    claude_tools = []
    for tool in mcp_tools:
        claude_tools.append({
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["inputSchema"],
        })
    return claude_tools


async def handle_chat(request: Request) -> JSONResponse:
    """
    POST /api/chat
    Body: { messages: [{role, content}], bot_name?: str }
    Response: { success, response, tools_used }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            {"success": False, "error": "JSON inválido"},
            status_code=400,
        )

    messages = body.get("messages", [])
    if not messages:
        return JSONResponse(
            {"success": False, "error": "Se requiere al menos un mensaje"},
            status_code=400,
        )

    bot_name = body.get("bot_name")
    system = SYSTEM_PROMPT
    if bot_name:
        system += f"\n\nEl usuario está trabajando con el bot: '{bot_name}'."

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "tu-api-key-aca":
        return JSONResponse(
            {"success": False, "error": "ANTHROPIC_API_KEY no configurada en .env"},
            status_code=500,
        )

    client = anthropic.Anthropic(api_key=api_key)
    claude_tools = _convert_tools_for_claude(TOOL_DEFINITIONS)
    tools_used = []

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=4096,
                system=system,
                tools=claude_tools,
                messages=messages,
            )

            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            if response.stop_reason == "end_turn" or not tool_use_blocks:
                text_parts = [b.text for b in response.content if b.type == "text"]
                final_text = "\n".join(text_parts) if text_parts else ""
                break


            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for tool_block in tool_use_blocks:
                tool_name = tool_block.name
                tool_args = tool_block.input
                tools_used.append(tool_name)

                print(f"🤖 Claude pidió: {tool_name}({tool_args})")

                try:
                    result_text = await dispatch_tool(tool_name, tool_args)
                except Exception as e:
                    result_text = f"Error ejecutando {tool_name}: {str(e)}"

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": str(result_text),
                })

            messages.append({"role": "user", "content": tool_results})

        else:
            final_text = "Se alcanzó el límite de ejecuciones de herramientas."

        return JSONResponse({
            "success": True,
            "response": final_text,
            "tools_used": tools_used,
        })

    except anthropic.APIError as e:
        return JSONResponse(
            {"success": False, "error": f"Error de Claude API: {str(e)}"},
            status_code=502,
        )
    except Exception as e:
        return JSONResponse(
            {"success": False, "error": f"Error interno: {str(e)}"},
            status_code=500,
        )
