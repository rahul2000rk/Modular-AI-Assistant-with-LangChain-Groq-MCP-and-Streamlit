from mcp.server.fastmcp import FastMCP
import requests
import os

from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("WeatherTool")

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the real-time weather for a given city using OpenWeatherMap."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return f"Could not find weather for '{location}': {data.get('message', 'Unknown error')}"

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return (f"The weather in {location.title()} is currently **{weather}** with a temperature of "
                f"**{temp}°C** (feels like {feels_like}°C). Humidity is {humidity}%, "
                f"and wind speed is {wind} m/s.")
    except Exception as e:
        return f"Error getting weather: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")


