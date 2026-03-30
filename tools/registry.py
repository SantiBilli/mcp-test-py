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
]
