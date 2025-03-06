from mcp.server.fastmcp import FastMCP, Context

def register_wait_tools(mcp: FastMCP):
    @mcp.tool()
    async def wait_for_element(selector: str, ctx: Context, timeout: int = 10) -> str:
        """Wait for an element to appear on the page
        
        Args:
            selector: CSS selector or XPath of the element to wait for
            timeout: Maximum time to wait in seconds
        """
        browser = ctx.request_context.lifespan_context["browser"]
        try:
            await browser.wait_for(selector, timeout=timeout)
            return f"Element appeared: {selector}"
        except Exception as e:
            return f"Timeout waiting for element: {selector}"
