import httpx
from tools.onedrive import get_access_token


async def get_bots_list_json() -> list:
    token = await get_access_token()
    url = "https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles:/children"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(url, headers=headers)

        if res.status_code == 404:
            return []

        res.raise_for_status()
        data = res.json()

        archivos = data.get("value", [])

        return [
            {"name": file.get("name", "").replace(".json", ""), "id": file.get("id", "")}
            for file in archivos if file.get("name", "").endswith(".json")
        ]


async def get_bot_data_json(filename: str) -> dict:
    token = await get_access_token()
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/AutoClickFiles/{filename}.json:/content"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(url, headers=headers)
        if res.status_code == 404:
            return None
        res.raise_for_status()
        return res.json()
