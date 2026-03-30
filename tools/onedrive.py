import os
import json
import httpx
import uuid 

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