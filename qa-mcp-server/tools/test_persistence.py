import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP, Context

def register_persistence_tools(mcp: FastMCP):
    @mcp.tool()
    async def save_test_case(test_name: str, ctx: Context, file_path: str = None) -> str:
        """Save a test case to a file
        
        Args:
            test_name: Name of the test case to save
            file_path: Path to save the test case (defaults to test_name.json)
        """
        test_cases = ctx.request_context.lifespan_context.get("test_cases", {})
        
        if test_name not in test_cases:
            return f"Test case '{test_name}' not found"
            
        if not file_path:
            file_path = f"{test_name.replace(' ', '_').lower()}.json"
            
        # Convert datetime objects to strings
        test_case = test_cases[test_name].copy()
        test_case["created_at"] = test_case["created_at"].isoformat()
        
        with open(file_path, "w") as f:
            json.dump(test_case, f, indent=2)
            
        return f"Saved test case to {file_path}"
        
    @mcp.tool()
    async def load_test_case(file_path: str, ctx: Context) -> str:
        """Load a test case from a file
        
        Args:
            file_path: Path to the test case file
        """
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
            
        with open(file_path, "r") as f:
            test_case = json.load(f)
            
        # Parse datetime string back to datetime object
        test_case["created_at"] = datetime.fromisoformat(test_case["created_at"])
        
        test_cases = ctx.request_context.lifespan_context.get("test_cases", {})
        test_cases[test_case["name"]] = test_case
        ctx.request_context.lifespan_context["test_cases"] = test_cases
        
        return f"Loaded test case: {test_case['name']}"
