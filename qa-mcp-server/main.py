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
from tools.forms import register_form_tools
from tools.network import register_network_tools
from tools.accessibility import register_accessibility_tools
from tools.test_definition import register_test_definition_tools
from tools.test_persistence import register_persistence_tools
from tools.nl_test_gen import register_nl_test_tools

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
register_form_tools(mcp)
register_network_tools(mcp)
register_accessibility_tools(mcp)
register_test_definition_tools(mcp)
register_persistence_tools(mcp)
register_nl_test_tools(mcp)

# Add lifespan after creating the server
mcp.lifespan = app_lifespan

if __name__ == "__main__":
    mcp.run()
