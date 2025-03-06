from mcp.server.fastmcp import FastMCP, Context

def register_assertion_tools(mcp: FastMCP):
    @mcp.tool()
    async def assert_element_exists(selector: str, ctx: Context) -> str:
        """Check if an element exists on the page
        
        Args:
            selector: CSS selector or XPath of the element to check
        """
        browser = ctx.request_context.lifespan_context["browser"]
        exists = await browser.exists(selector)
        if exists:
            return f"✅ Element exists: {selector}"
        else:
            return f"❌ Element does not exist: {selector}"
        
    @mcp.tool()
    async def assert_text_contains(selector: str, text: str, ctx: Context) -> str:
        """Check if an element contains specific text
        
        Args:
            selector: CSS selector or XPath of the element
            text: Text to check for
        """
        browser = ctx.request_context.lifespan_context["browser"]
        element_text = await browser.text(selector)
        if text in element_text:
            return f"✅ Element contains text '{text}'"
        else:
            return f"❌ Element does not contain text '{text}'"
