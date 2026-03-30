import os
import json
import httpx

CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("MICROSOFT_REFRESH_TOKEN")

async def get_access_token():
    """Genera un access token temporal usando el refresh token."""
    print("\n" + "="*40)
    print(f"🔍 DIAGNÓSTICO DE LLAVES:")
    print(f"ID: {str(CLIENT_ID)[:5]}... (Longitud: {len(str(CLIENT_ID))})")
    print(f"SECRET: {str(CLIENT_SECRET)[:3]}... (Longitud: {len(str(CLIENT_SECRET))})")
    print(f"TOKEN: {str(REFRESH_TOKEN)[:5]}... (Longitud: {len(str(REFRESH_TOKEN))})")
    
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(url, data=data)
        
        if res.status_code != 200:
            print(f"🚨 RECHAZO DE MICROSOFT: {res.text}")
            print("="*40 + "\n")
            raise Exception(f"Microsoft rechazó el acceso: {res.text}")
            
        print("✅ Token temporal generado con éxito.")
        print("="*40 + "\n")
        return res.json()["access_token"]

async def create_json_onedrive(filename: str, initial_data: dict) -> str:
    """Crea un archivo JSON en la carpeta AutoClickFiles de OneDrive."""
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        res = await client.put(url, headers=headers, content=json.dumps(initial_data, indent=4))
        res.raise_for_status()
    return f"✅ Archivo {filename}.json creado exitosamente en tu carpeta AutoClickFiles de OneDrive."

async def modify_json_onedrive(filename: str, key: str, value: str) -> str:
    """Modifica o agrega un valor en un archivo JSON existente en AutoClickFiles."""
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        get_res = await client.get(url, headers=headers)
        if get_res.status_code == 404:
            return f"❌ Error: El archivo {filename}.json no existe en OneDrive."
        get_res.raise_for_status()
        data = get_res.json()
        
        data[key] = value
        
        headers["Content-Type"] = "application/json"
        put_res = await client.put(url, headers=headers, content=json.dumps(data, indent=4))
        put_res.raise_for_status()
    return f"✅ Archivo {filename}.json modificado. Clave '{key}' actualizada a '{value}'."

async def delete_json_onedrive(filename: str) -> str:
    """Elimina un archivo JSON de la carpeta AutoClickFiles en OneDrive."""
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        res = await client.delete(url, headers=headers)
        if res.status_code == 404:
            return f"❌ Error: El archivo {filename}.json no existe."
        res.raise_for_status()
    return f"🗑️ Archivo {filename}.json eliminado correctamente de OneDrive."
