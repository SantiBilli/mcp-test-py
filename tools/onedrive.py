import os
import json
import httpx
import uuid 
import ast

CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("MICROSOFT_REFRESH_TOKEN")

async def get_access_token():
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(url, data=data)
        if res.status_code != 200:
            raise Exception(f"Microsoft rechazó el acceso: {res.text}")
        return res.json()["access_token"]


async def create_json_onedrive(filename: str) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    
    bot_id = f"BOT_{uuid.uuid4().hex[:6].upper()}"
    
    data = {
        "id": bot_id,
        "nombre": filename,
        "bloques": []
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        res = await client.put(url, headers=headers, content=json.dumps(data, indent=4))
        res.raise_for_status()

    return f"✅ Archivo {filename}.json creado. ID: {bot_id}"


async def read_json_onedrive(filename: str) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(url, headers=headers)
        if res.status_code == 404:
            return f"❌ {filename}.json no existe"
        
        res.raise_for_status()
        contenido = json.dumps(res.json(), indent=4)

    return f"📄 {filename}.json:\n```json\n{contenido}\n```"


async def modify_json_onedrive(filename: str, key: str, value) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(url, headers=headers)
        if res.status_code == 404:
            return f"❌ {filename}.json no existe"
        
        res.raise_for_status()
        data = res.json()

        data[key] = value

        headers["Content-Type"] = "application/json"
        await client.put(url, headers=headers, content=json.dumps(data, indent=4))

    return f"✅ {filename}.json actualizado"


async def delete_json_onedrive(filename: str) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        res = await client.delete(url, headers=headers)
        if res.status_code == 404:
            return f"❌ {filename}.json no existe"
        
        res.raise_for_status()

    return f"🗑️ {filename}.json eliminado"


async def rename_json_onedrive(old_filename: str, new_filename: str) -> str:
    token = await get_access_token()

    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        meta_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{old_filename}.json"
        meta_res = await client.get(meta_url, headers=headers)

        if meta_res.status_code == 404:
            return f"❌ {old_filename}.json no existe"

        meta_res.raise_for_status()
        file_id = meta_res.json()["id"]

        patch_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
        await client.patch(
            patch_url,
            headers={**headers, "Content-Type": "application/json"},
            json={"name": f"{new_filename}.json"}
        )

        content_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
        res = await client.get(content_url, headers=headers)
        res.raise_for_status()

        data = res.json()

        data["nombre"] = new_filename

        await client.put(
            content_url,
            headers={**headers, "Content-Type": "application/json"},
            content=json.dumps(data, indent=4)
        )

    return f"✅ Renombrado a {new_filename}.json correctamente"


async def add_blocks_to_bot(filename: str, nuevos_bloques, insert_after_id: str = "") -> str:
    # ESCUDO ANTI-IA: Si Copilot manda un String mal formateado, lo forzamos a Lista
    if isinstance(nuevos_bloques, str):
        try:
            nuevos_bloques = json.loads(nuevos_bloques.replace("'", '"'))
        except:
            nuevos_bloques = ast.literal_eval(nuevos_bloques)

    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        get_res = await client.get(url, headers=headers)
        if get_res.status_code == 404:
            return f"❌ Error: El bot {filename} no existe."
        get_res.raise_for_status()
        data = get_res.json()
        
        for bloque in nuevos_bloques:
            if "id" not in bloque:
                bloque["id"] = f"blk_{uuid.uuid4().hex[:6]}"
        
        lista_bloques = data.get("bloques", [])
        indice_insercion = len(lista_bloques)
        
        if insert_after_id:
            for i, bloque in enumerate(lista_bloques):
                if bloque.get("id") == insert_after_id:
                    indice_insercion = i + 1
                    break
        
        lista_bloques[indice_insercion:indice_insercion] = nuevos_bloques
        
        for i, b in enumerate(lista_bloques):
            b["position"] = i
            
        data["bloques"] = lista_bloques
        
        headers["Content-Type"] = "application/json"
        put_res = await client.put(url, headers=headers, content=json.dumps(data, indent=4))
        put_res.raise_for_status()
        
    nombres = ", ".join([b.get("tipo", "desconocido") for b in nuevos_bloques])
    return f"✅ Se agregaron los bloques ({nombres}) al bot {filename}."

async def remove_block_from_bot(filename: str, block_id: str) -> str:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        get_res = await client.get(url, headers=headers)
        get_res.raise_for_status()
        data = get_res.json()
        
        lista_bloques = data.get("bloques", [])
        nueva_lista = [b for b in lista_bloques if b.get("id") != block_id]
        
        if len(lista_bloques) == len(nueva_lista):
            return f"⚠️ No se encontró ningún bloque con el ID {block_id}."
            
        for i, b in enumerate(nueva_lista):
            b["position"] = i
            
        data["bloques"] = nueva_lista
        
        headers["Content-Type"] = "application/json"
        await client.put(url, headers=headers, content=json.dumps(data, indent=4))
        
    return f"🗑️ Bloque {block_id} eliminado exitosamente."