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
        "description": "Agrega acciones al bot. ¡CRÍTICO: Rellena SIEMPRE el objeto 'parametros'!",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "nuevos_bloques": {
                    "type": "array", 
                    "description": "Lista de bloques a insertar.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "tipo": {
                                "type": "string", 
                                "description": "El tipo de bloque: inicio, accion, espera, mensaje, condicion o fin."
                            },
                            "parametros": {
                                "type": "object",
                                "description": "Objeto con los valores del bloque. NUNCA VACÍO para accion o espera.",
                                "properties": {
                                    "x": {"type": "integer"},
                                    "y": {"type": "integer"},
                                    "boton": {"type": "string"},
                                    "tipo_click": {"type": "string"},
                                    "tiempo_ms": {"type": "integer"},
                                    "tecla_activacion": {"type": "string"},
                                    "texto": {"type": "string"},
                                    "color_esperado_hex": {"type": "string"},
                                    "siguiente_bloque_si_cumple": {"type": "string"},
                                    "siguiente_bloque_si_falla": {"type": "string"}
                                }
                            }
                        },
                        "required": ["tipo", "parametros"]
                    }
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
    }
]
