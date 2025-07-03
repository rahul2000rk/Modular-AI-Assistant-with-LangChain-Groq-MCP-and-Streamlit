from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WeatherTool")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for a location"""
    return f"The weather in {location} is sunny with clear skies (demo)."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
