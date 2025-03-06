from mcp.server.fastmcp import FastMCP
from tools.navigation import register_navigation_tools

# Initialize MCP server
mcp = FastMCP(
    "QA-E2E-Testing",
    dependencies=["browser-use==0.1.37"]  # Use 0.1.37 to avoid API issues
)

# Register tool modules
register_navigation_tools(mcp)

if __name__ == "__main__":
    mcp.run()
