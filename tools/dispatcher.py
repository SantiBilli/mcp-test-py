"""
Dispatcher de herramientas MCP.
Mapea el nombre de cada tool a la función que la ejecuta.
"""

from tools.onedrive import (
    create_json_onedrive,
    read_json_onedrive,
    modify_json_onedrive,
    delete_json_onedrive,
    rename_json_onedrive,
)
from tools.get_weather import handle_get_weather


async def dispatch_tool(tool_name: str, args: dict) -> str:
    if tool_name == "get_weather":
        res = await handle_get_weather(args.get("city"))
        return res[0].text

    if tool_name == "create_json_onedrive":
        return await create_json_onedrive(args.get("filename"))

    if tool_name == "read_json_onedrive":
        return await read_json_onedrive(args.get("filename"))

    if tool_name == "modify_json_onedrive":
        return await modify_json_onedrive(
            args.get("filename"),
            args.get("key"),
            str(args.get("value")),
        )

    if tool_name == "delete_json_onedrive":
        return await delete_json_onedrive(args.get("filename"))

    if tool_name == "rename_json_onedrive":
        return await rename_json_onedrive(
            args.get("old_filename"),
            args.get("new_filename"),
        )

    raise ValueError(f"Herramienta '{tool_name}' no encontrada.")
