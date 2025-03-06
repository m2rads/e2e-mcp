from mcp.server.fastmcp import FastMCP
from tools.navigation import register_navigation_tools
from contextlib import asynccontextmanager
from typing import AsyncIterator
from server.browser_manager import browser_lifespan

# Initialize MCP server
mcp = FastMCP(
    "QA-E2E-Testing",
    dependencies=["browser-use==0.1.37"],  # Use 0.1.37 to avoid API issues
    lifespan=app_lifespan
)

# Register tool modules
register_navigation_tools(mcp)

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage application lifecycle"""
    async with browser_lifespan() as browser:
        yield {"browser": browser}

if __name__ == "__main__":
    mcp.run()
