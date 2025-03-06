from mcp.server.fastmcp import FastMCP, Context
from datetime import datetime

def register_test_tools(mcp: FastMCP):
    @mcp.tool()
    async def start_test_session(name: str, ctx: Context) -> str:
        """Start a new test session
        
        Args:
            name: Name of the test session
        """
        browser = ctx.request_context.lifespan_context["browser"]
        ctx.request_context.lifespan_context["test_session"] = {
            "name": name,
            "steps": [],
            "started_at": datetime.now(),
            "status": "running"
        }
        return f"Started test session: {name}"
        
    @mcp.tool()
    async def record_test_step(description: str, ctx: Context, status: str = "passed") -> str:
        """Record a test step in the current session
        
        Args:
            description: Description of the test step
            status: Status of the step (passed/failed/skipped)
        """
        session = ctx.request_context.lifespan_context.get("test_session")
        if not session:
            return "No active test session"
            
        session["steps"].append({
            "description": description,
            "status": status,
            "timestamp": datetime.now()
        })
        return f"Recorded step: {description} ({status})"
        
    @mcp.tool()
    async def end_test_session(ctx: Context, status: str = "passed") -> str:
        """End the current test session
        
        Args:
            status: Final status of the test session
        """
        session = ctx.request_context.lifespan_context.get("test_session")
        if not session:
            return "No active test session"
            
        session["status"] = status
        session["ended_at"] = datetime.now()
        
        # Generate report
        report = f"Test Report: {session['name']}\n"
        report += f"Status: {session['status']}\n"
        report += f"Duration: {session['ended_at'] - session['started_at']}\n"
        report += "Steps:\n"
        
        for i, step in enumerate(session["steps"], 1):
            report += f"{i}. {step['description']} - {step['status']}\n"
            
        ctx.request_context.lifespan_context["test_session"] = None
        return report
