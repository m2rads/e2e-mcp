from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from typing import AsyncIterator
from server.browser_manager import browser_lifespan
from tools.navigation import register_navigation_tools
from tools.interaction import register_interaction_tools
from tools.assertions import register_assertion_tools
from tools.waits import register_wait_tools
from tools.test_runner import register_test_tools
from tools.screenshots import register_screenshot_tools

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage application lifecycle"""
    async with browser_lifespan() as browser:
        yield {"browser": browser}

# Initialize MCP server
mcp = FastMCP(
    "QA-E2E-Testing",
    dependencies=["browser-use", "httpx"],
)

# Register tool modules
register_navigation_tools(mcp)
register_interaction_tools(mcp)
register_assertion_tools(mcp)
register_wait_tools(mcp)
register_test_tools(mcp)
register_screenshot_tools(mcp)

# Add lifespan after creating the server
mcp.lifespan = app_lifespan

if __name__ == "__main__":
    mcp.run()
