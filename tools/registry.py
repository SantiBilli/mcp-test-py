TOOL_DEFINITIONS = [
    {
        "name": "get_weather",
        "description": "Obtiene el clima actual de una ciudad",
        "inputSchema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Nombre de la ciudad"}
            },
            "required": ["city"],
        },
    },
    {
        "name": "create_json_onedrive",
        "description": "Crea un nuevo archivo JSON base en OneDrive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Nombre del archivo (sin .json)",
                }
            },
            "required": ["filename"],
        },
    },
    {
        "name": "read_json_onedrive",
        "description": "Lee un archivo JSON desde OneDrive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Nombre del archivo (sin .json)",
                }
            },
            "required": ["filename"],
        },
    },
    {
        "name": "delete_json_onedrive",
        "description": "Elimina un archivo JSON de OneDrive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Nombre del archivo",
                }
            },
            "required": ["filename"],
        },
    },
    {
        "name": "rename_json_onedrive",
        "description": "Renombra un archivo JSON y actualiza su nombre interno",
        "inputSchema": {
            "type": "object",
            "properties": {
                "old_filename": {
                    "type": "string",
                    "description": "Nombre actual",
                },
                "new_filename": {
                    "type": "string",
                    "description": "Nuevo nombre",
                },
            },
            "required": ["old_filename", "new_filename"],
        },
    },
    {
        "name": "modify_json_onedrive",
        "description": "Modifica propiedades generales del archivo (como el 'nombre'). NUNCA uses esta herramienta para modificar el array de 'bloques'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "key": {"type": "string", "description": "Propiedad a modificar (NUNCA usar 'bloques')"},
                "value": {"description": "Nuevo valor"}
            },
            "required": ["filename", "key", "value"],
        },
    },
    {
        "name": "add_blocks_to_bot",
        "description": "Agrega acciones al bot. ¡CRÍTICO: 'nuevos_bloques' debe ser enviado como un STRING en formato JSON, no como un array nativo!",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "nuevos_bloques": {
                    "type": "string", 
                    "description": "Un STRING de texto que contiene el JSON array con los bloques. Ejemplo: '[{\"tipo\": \"espera\", \"parametros\": {\"tiempo_ms\": 500}}]'. Asegúrate de incluir todos los parámetros."
                },
                "insert_after_id": {
                    "type": "string", 
                    "description": "(Opcional) ID del bloque posterior."
                }
            },
            "required": ["filename", "nuevos_bloques"]
        }
    },
    {
        "name": "remove_block_from_bot",
        "description": "Elimina un bloque específico del bot usando su ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "block_id": {"type": "string", "description": "El ID exacto del bloque a borrar (ej: blk_a1b2)"}
            },
            "required": ["filename", "block_id"]
        }
    },
    {
        "name": "list_bots_onedrive",
        "description": "Obtiene la lista de todos los bots guardados en la carpeta. Úsala cuando el usuario te pida ver qué bots tiene disponibles.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]