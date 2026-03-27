import httpx
from mcp.types import TextContent

async def handle_get_weather(city: str) -> list[TextContent]:
    """
    Obtener el clima actual de una ciudad específica usando Open-Meteo API.
    """
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=es&format=json"
        
        async with httpx.AsyncClient() as client:
            geo_response = await client.get(geo_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if "results" not in geo_data or len(geo_data["results"]) == 0:
                raise ValueError(f"No se encontró la ciudad: {city}")
                
            result = geo_data["results"][0]
            latitude = result["latitude"]
            longitude = result["longitude"]
            name = result["name"]
            country = result.get("country", "")
            
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            weather_response = await client.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            temp = weather_data["current_weather"]["temperature"]
            windspeed = weather_data["current_weather"]["windspeed"]
            
            return [
                TextContent(
                    type="text",
                    text=f"El clima en {name}, {country} es de {temp}°C con una velocidad de viento de {windspeed} km/h."
                )
            ]
            
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error al obtener el clima: {str(e)}"
            )
        ]
