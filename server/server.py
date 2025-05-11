from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import dotenv_values

mcp = FastMCP("weather")

config = dotenv_values(".env")
API_KEY = config["API_KEY"]
BASE_URL = config["BASE_URL"]
USER_AGENT = config["USER_AGENT"]

async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching weather data: {str(e)}")
            return None
        
def format_current_weather(data: dict) -> str:
    """Format current weather data into a readable string."""
    location = data.get("location", {})
    current = data.get("current", {})
    return f"""
        City: {location.get('name', 'Unknown')}
        Country: {location.get('country', 'Unknown')}
        Weather: {current.get('condition', {}).get('text', 'Unknown')}
        Temperature: {current.get('temp_c', 'Unknown')}°C
        Wind: {current.get('wind_kph', 'Unknown')} km/h
        Humidity: {current.get('humidity', 'Unknown')}%
        """

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: it is string value that represents the city name (e.g. London, Patna, etc.)
    """
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}&aqi=no"
    data = await make_nws_request(url)

    if not data:
        return "Unable to fetch weather data."

    return format_current_weather(data)
