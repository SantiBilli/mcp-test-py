import os
import aiofiles
from mcp.types import TextContent

async def handle_create_file(dir_path: str, name: str) -> list[TextContent]:
    try:
        full_path = os.path.join(dir_path, f"{name}.txt")
        print(f"Dir Path... {dir_path} Name... {name} Full Path... {full_path}")
        
        os.makedirs(dir_path, exist_ok=True)
        
        async with aiofiles.open(full_path, mode='w') as f:
            await f.write("")
            
        return [
            TextContent(
                type="text",
                text=f"File {full_path} created successfully"
            )
        ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Failed to create file: {str(e)}"
            )
        ]
