import httpx
import asyncio


async def test_chat():
    async with httpx.AsyncClient(timeout=30) as client:
        print("--- Test 1: Saludo ---")
        r = await client.post(
            "http://localhost:8000/api/chat",
            json={"messages": [{"role": "user", "content": "Hola, que podes hacer?"}]},
        )
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Success: {data.get('success')}")
        print(f"Response: {data.get('response', data.get('error'))}")
        print(f"Tools used: {data.get('tools_used')}")


asyncio.run(test_chat())
