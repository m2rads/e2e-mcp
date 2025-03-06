from mcp.server.fastmcp import FastMCP, Context, Image
import base64
from datetime import datetime

def register_screenshot_tools(mcp: FastMCP):
    @mcp.tool()
    async def take_screenshot(ctx: Context, name: str = None) -> Image:
        """Take a screenshot of the current page state
        
        Args:
            name: Optional name for the screenshot
        """
        browser = ctx.request_context.lifespan_context["browser"]
        screenshot_data = await browser.screenshot()
        
        # If in a test session, store the screenshot
        session = ctx.request_context.lifespan_context.get("test_session")
        if session:
            if not name:
                name = f"screenshot_{len(session['steps'])}"
                
            # Store screenshot reference in session
            if "screenshots" not in session:
                session["screenshots"] = []
                
            session["screenshots"].append({
                "name": name,
                "timestamp": datetime.now()
            })
        
        return Image(data=screenshot_data, format="png")
