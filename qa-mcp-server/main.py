# IMPORTANT: Load logging configuration first, before any other imports
from server.logging_config import configure_logging
configure_logging()

# Now regular imports
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from typing import AsyncIterator
from server.browser_manager import browser_lifespan
from tools.navigation import register_navigation_tools
from tools.interaction import register_interaction_tools
from tools.assertions import register_assertion_tools
from tools.waits import register_wait_tools
from tools.test_runner import register_test_tools
from tools.forms import register_form_tools
from tools.network import register_network_tools
from tools.accessibility import register_accessibility_tools
from tools.test_definition import register_test_definition_tools
from tools.test_persistence import register_persistence_tools
from tools.nl_test_gen import register_nl_test_tools
from tools.visual_regression import register_visual_tools
from tools.browser_state import register_browser_state_tools
from tools.ci_integration import register_ci_tools

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage application lifecycle"""
    async with browser_lifespan() as browser:
        # Initialize test state storage
        yield {
            "browser": browser,
            "test_cases": {},
            "test_session": None
        }

# Initialize MCP server
mcp = FastMCP(
    "QA-E2E-Testing",
    dependencies=["browser-use", "httpx"],
)

# Register tool modules - with the correct function names
register_navigation_tools(mcp)
register_interaction_tools(mcp)
register_wait_tools(mcp)
register_assertion_tools(mcp)
register_test_tools(mcp)
register_form_tools(mcp)
register_network_tools(mcp)
register_accessibility_tools(mcp)
register_test_definition_tools(mcp)
register_persistence_tools(mcp)
register_nl_test_tools(mcp)
register_visual_tools(mcp)
register_browser_state_tools(mcp)
register_ci_tools(mcp)

# Add lifespan after creating the server
mcp.lifespan = app_lifespan

if __name__ == "__main__":
    mcp.run()
