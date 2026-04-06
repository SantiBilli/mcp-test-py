async def dispatch_tool(tool_name: str, args: dict) -> str:
    user_token = args.get("user_token")

    if tool_name == "get_weather":
        res = await handle_get_weather(args.get("city"), user_token) 
        if isinstance(res, list): 
            return res[0].text
        return res

    if tool_name == "create_json_onedrive":
        return await create_json_onedrive(args.get("filename"), user_token)

    if tool_name == "read_json_onedrive":
        return await read_json_onedrive(args.get("filename"), user_token)

    if tool_name == "modify_json_onedrive":
        return await modify_json_onedrive(
            args.get("filename"),
            args.get("key"),
            args.get("value"),
            user_token
        )

    if tool_name == "delete_json_onedrive":
        return await delete_json_onedrive(args.get("filename"), user_token)

    if tool_name == "rename_json_onedrive":
        return await rename_json_onedrive(
            args.get("old_filename"),
            args.get("new_filename"),
            user_token
        )
    
    if tool_name == "add_blocks_to_bot":
        return await add_blocks_to_bot(
            args.get("filename"),
            args.get("nuevos_bloques"),
            user_token,
            args.get("insert_after_id", "")
        )

    if tool_name == "remove_block_from_bot":
        return await remove_block_from_bot(
            args.get("filename"),
            args.get("block_id"),
            user_token
        )

    if tool_name == "list_bots_onedrive":
        return await list_bots_onedrive(user_token)

    raise ValueError(f"Herramienta '{tool_name}' no encontrada.")