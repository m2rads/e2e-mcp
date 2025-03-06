from mcp.server.fastmcp import FastMCP, Context

def register_navigation_tools(mcp: FastMCP):
    @mcp.tool()
    async def navigate_to(url: str, ctx: Context) -> str:
        """Navigate to a specific URL
        
        Args:
            url: The URL to navigate to
        """
        agent = ctx.request_context.lifespan_context["browser"]
        # Navigate using the browser instance
        await agent.browser.goto(url)
        return f"Navigated to {url}"
    
    @mcp.tool()
    async def get_current_url(ctx: Context) -> str:
        """Get the current page URL"""
        agent = ctx.request_context.lifespan_context["browser"]
        current_url = await agent.browser.current_url()
        return current_url
    
    @mcp.tool()
    async def get_page_title(ctx: Context) -> str:
        """Get the current page title"""
        agent = ctx.request_context.lifespan_context["browser"]
        title = await agent.browser.title()
        return title
