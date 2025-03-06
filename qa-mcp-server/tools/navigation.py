from mcp.server.fastmcp import FastMCP, Context

def register_navigation_tools(mcp: FastMCP):
    @mcp.tool()
    async def navigate_to(url: str, ctx: Context) -> str:
        """Navigate to a specific URL
        
        Args:
            url: The URL to navigate to
        """
        browser = ctx.request_context.lifespan_context["browser"]
        await browser.navigate(url)
        return f"Navigated to {url}"
