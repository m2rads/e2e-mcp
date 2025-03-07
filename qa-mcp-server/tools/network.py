from mcp.server.fastmcp import FastMCP, Context

def register_network_tools(mcp: FastMCP):
    @mcp.tool()
    async def wait_for_network_idle(ctx: Context, timeout: int = 5000) -> str:
        """Wait for network activity to become idle
        
        Args:
            timeout: Maximum time to wait in milliseconds
        """
        browser = ctx.request_context.lifespan_context["browser"]
        await browser.wait_for_network_idle(timeout)
        return "Network is idle"
        
    @mcp.tool()
    async def intercept_requests(patterns: list[str], ctx: Context) -> str:
        """Start intercepting network requests matching patterns
        
        Args:
            patterns: List of URL patterns to intercept
        """
        browser = ctx.request_context.lifespan_context["browser"]
        # Store in context that we want to collect these
        ctx.request_context.lifespan_context["network_intercepts"] = patterns
        
        # Set up intercepts in browser-use
        # Implementation details will depend on browser-use capabilities
        
        return f"Intercepting requests: {', '.join(patterns)}"
        
    @mcp.tool()
    async def get_intercepted_requests(ctx: Context) -> str:
        """Get all intercepted requests"""
        browser = ctx.request_context.lifespan_context["browser"]
        # Implement based on browser-use capabilities
        # For now, return placeholder
        return "Intercepted requests data would appear here"
