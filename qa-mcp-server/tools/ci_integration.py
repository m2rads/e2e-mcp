import json
from mcp.server.fastmcp import FastMCP, Context

def register_ci_tools(mcp: FastMCP):
    @mcp.tool()
    async def export_test_results(ctx: Context, format: str = "json") -> str:
        """Export test results in a format suitable for CI systems
        
        Args:
            format: Output format (json/junit)
        """
        session = ctx.request_context.lifespan_context.get("test_session")
        if not session or session["status"] != "finished":
            return "No completed test session available"
            
        if format == "json":
            # Return JSON format
            return json.dumps(session, default=str)
        elif format == "junit":
            # Return JUnit XML format
            # Implementation details omitted
            return "<xml>JUnit format would go here</xml>"
        else:
            return f"Unsupported format: {format}"
