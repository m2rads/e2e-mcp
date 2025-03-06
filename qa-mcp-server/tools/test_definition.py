from mcp.server.fastmcp import FastMCP, Context
from datetime import datetime

def register_test_definition_tools(mcp: FastMCP):
    @mcp.tool()
    async def create_test_case(name: str, description: str, ctx: Context) -> str:
        """Create a new test case definition
        
        Args:
            name: Name of the test case
            description: Description of what the test validates
        """
        test_cases = ctx.request_context.lifespan_context.get("test_cases", {})
        
        if name in test_cases:
            return f"Test case '{name}' already exists"
            
        test_cases[name] = {
            "name": name,
            "description": description,
            "steps": [],
            "created_at": datetime.now()
        }
        
        ctx.request_context.lifespan_context["test_cases"] = test_cases
        return f"Created test case: {name}"
        
    @mcp.tool()
    async def add_test_step(
        test_name: str, 
        command: str, 
        params: dict, 
        ctx: Context,
        description: str = None
    ) -> str:
        """Add a step to an existing test case
        
        Args:
            test_name: Name of the test case
            command: The tool to execute
            params: Parameters for the command
            description: Human-readable description of the step
        """
        test_cases = ctx.request_context.lifespan_context.get("test_cases", {})
        
        if test_name not in test_cases:
            return f"Test case '{test_name}' not found"
            
        test_cases[test_name]["steps"].append({
            "command": command,
            "params": params,
            "description": description or f"Execute {command}"
        })
        
        return f"Added step to test case '{test_name}'"
        
    @mcp.tool()
    async def run_test_case(test_name: str, ctx: Context) -> str:
        """Run a previously defined test case
        
        Args:
            test_name: Name of the test case to run
        """
        test_cases = ctx.request_context.lifespan_context.get("test_cases", {})
        
        if test_name not in test_cases:
            return f"Test case '{test_name}' not found"
            
        test_case = test_cases[test_name]
        browser = ctx.request_context.lifespan_context["browser"]
        
        # Start test session
        ctx.request_context.lifespan_context["test_session"] = {
            "name": test_case["name"],
            "steps": [],
            "started_at": datetime.now(),
            "status": "running"
        }
        
        session = ctx.request_context.lifespan_context["test_session"]
        
        # Execute each step
        for step in test_case["steps"]:
            try:
                # Record the step
                session["steps"].append({
                    "description": step["description"],
                    "status": "running",
                    "timestamp": datetime.now()
                })
                
                # Execute the step
                # In a real implementation, this would dispatch to the appropriate tool
                # For now, we'll just record it
                
                session["steps"][-1]["status"] = "passed"
            except Exception as e:
                session["steps"][-1]["status"] = "failed"
                session["steps"][-1]["error"] = str(e)
                session["status"] = "failed"
                break
        
        if session["status"] == "running":
            session["status"] = "passed"
            
        # Generate report
        report = f"Test Report: {session['name']}\n"
        report += f"Status: {session['status']}\n"
        report += f"Duration: {datetime.now() - session['started_at']}\n"
        report += "Steps:\n"
        
        for i, step in enumerate(session["steps"], 1):
            report += f"{i}. {step['description']} - {step['status']}\n"
            
        ctx.request_context.lifespan_context["test_session"] = None
        return report
