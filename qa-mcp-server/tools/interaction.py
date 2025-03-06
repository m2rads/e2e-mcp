from mcp.server.fastmcp import FastMCP, Context

def register_interaction_tools(mcp: FastMCP):
    @mcp.tool()
    async def click_element(selector: str, ctx: Context) -> str:
        """Click on an element in the page
        
        Args:
            selector: CSS selector of the element to click
        """
        agent = ctx.request_context.lifespan_context["browser"]
        await agent.browser.click(selector)
        return f"Clicked element: {selector}"
    
    @mcp.tool()
    async def type_text(selector: str, text: str, ctx: Context) -> str:
        """Type text into an input field
        
        Args:
            selector: CSS selector of the input field
            text: Text to type
        """
        agent = ctx.request_context.lifespan_context["browser"]
        await agent.browser.fill(selector, text)
        return f"Typed '{text}' into {selector}"
    
    @mcp.tool()
    async def take_screenshot(ctx: Context) -> str:
        """Take a screenshot of the current page"""
        agent = ctx.request_context.lifespan_context["browser"]
        screenshot_path = "screenshot.png"
        await agent.browser.screenshot(path=screenshot_path)
        return f"Screenshot saved to {screenshot_path}"
