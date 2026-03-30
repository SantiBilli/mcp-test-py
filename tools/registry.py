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
        "name": "modify_json_onedrive",
        "description": "Modifica o agrega una propiedad en un JSON",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Nombre del archivo",
                },
                "key": {
                    "type": "string",
                    "description": "Propiedad a modificar",
                },
                "value": {
                    "description": "Nuevo valor (puede ser cualquier tipo JSON)"
                },
            },
            "required": ["filename", "key", "value"],
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
        "name": "add_blocks_to_bot",
        "description": "Agrega una lista de bloques al bot. Úsala siempre que el usuario pida agregar acciones.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "nuevos_bloques": {
                    "type": "array", 
                    "description": "Lista de objetos JSON de los bloques a agregar. No incluyas el campo 'id' ni 'position', el sistema los generará.",
                    "items": {"type": "object"}
                },
                "insert_after_id": {
                    "type": "string", 
                    "description": "(Opcional) El ID del bloque existente después del cual se deben insertar. Si está vacío, van al final."
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
    }
]
