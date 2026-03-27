import os
import aiofiles
from mcp.types import TextContent

async def handle_create_file(dir_path: str, name: str) -> list[TextContent]:
    """
    Creates a new text file at the specified directory path with the given name.
    """
    try:
        # Crea el nombre final del archivo (ej: nombre.txt)
        full_path = os.path.join(dir_path, f"{name}.txt")
        print(f"Dir Path... {dir_path} Name... {name} Full Path... {full_path}")
        
        # Crea el directorio si no existe (equivalente a recursive: true)
        os.makedirs(dir_path, exist_ok=True)
        
        # Crea el archivo vacío
        async with aiofiles.open(full_path, mode='w') as f:
            await f.write("")
            
        return [
            TextContent(
                type="text",
                text=f"File {full_path} created successfully"
            )
        ]
    except Exception as e:
        # En Python SDK, devolver isError se maneja levantando una excepción específica o estructurando el resultado.
        # Aquí retornaremos el texto como indicaba el código JS, marcándolo si es necesario.
        return [
            TextContent(
                type="text",
                text=f"Failed to create file: {str(e)}"
            )
        ]
