CATALOGO_BLOQUES = [
    {
        "modelo_id": "tpl_inicio",
        "tipo": "inicio",
        "descripcion": "Punto de partida del bot. Puede configurarse una tecla rápida para arrancar.",
        "parametros": {
            "tecla_activacion": "F5"
        }
    },
    {
        "modelo_id": "tpl_accion",
        "tipo": "accion",
        "descripcion": "Ejecuta un clic del mouse en coordenadas específicas de la pantalla.",
        "parametros": {
            "x": 0,
            "y": 0,
            "boton": "izquierdo",
            "tipo_click": "simple"
        }
    },
    {
        "modelo_id": "tpl_espera",
        "tipo": "espera",
        "descripcion": "Pausa la ejecución del bot por un tiempo determinado en milisegundos.",
        "parametros": {
            "tiempo_ms": 1000
        }
    },
    {
        "modelo_id": "tpl_condicion",
        "tipo": "condicion",
        "descripcion": "Verifica si un pixel en la pantalla es de cierto color para tomar una decisión lógica.",
        "parametros": {
            "x": 0,
            "y": 0,
            "color_esperado_hex": "#FFFFFF",
            "siguiente_bloque_si_cumple": "",
            "siguiente_bloque_si_falla": ""
        }
    },
    {
        "modelo_id": "tpl_mensaje",
        "tipo": "mensaje",
        "descripcion": "Muestra un texto en la consola del bot o en un log visible para el usuario.",
        "parametros": {
            "texto": "Acción completada con éxito."
        }
    },
    {
        "modelo_id": "tpl_fin",
        "tipo": "fin",
        "descripcion": "Detiene la ejecución completa del bot de forma segura.",
        "parametros": {}
    }
]