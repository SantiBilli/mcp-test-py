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
        "description": "Agrega bloques de acciones al bot. REGLA OBLIGATORIA: cada bloque DEBE incluir 'tipo' y 'parametros' con TODOS sus valores rellenados. Está PROHIBIDO enviar 'parametros' vacío ({}). Si el usuario dice click en x=100 y=200, el bloque debe tener parametros: {x: 100, y: 200, boton: 'izquierdo', tipo_click: 'simple'}.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "nuevos_bloques": {
                    "type": "array",
                    "description": "Array de bloques. No incluir 'id' ni 'position' (se generan automáticamente). OBLIGATORIO incluir 'parametros' completos en cada bloque.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "tipo": {
                                "type": "string",
                                "enum": ["inicio", "accion", "espera", "fin"],
                                "description": "Tipo de bloque"
                            },
                            "parametros": {
                                "type": "object",
                                "description": "OBLIGATORIO. Parámetros del bloque según su tipo. Para 'inicio': {tecla_activacion: string}. Para 'accion': {boton: 'izquierdo'|'derecho', tipo_click: 'simple'|'doble', x: number, y: number}. Para 'espera': {tiempo_ms: number}. Para 'fin': {}."
                            }
                        },
                        "required": ["tipo", "parametros"]
                    }
                },
                "insert_after_id": {
                    "type": "string",
                    "description": "(Opcional) ID del bloque después del cual insertar."
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
