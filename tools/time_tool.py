from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("TimeTool")

@mcp.tool()
def get_current_time() -> str:
    """Get the current time"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    mcp.run(transport="stdio")
