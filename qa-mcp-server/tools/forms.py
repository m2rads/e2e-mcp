from mcp.server.fastmcp import FastMCP, Context

def register_form_tools(mcp: FastMCP):
    @mcp.tool()
    async def fill_form(form_data: dict, ctx: Context) -> str:
        """Fill a form with the provided data
        
        Args:
            form_data: Dictionary mapping selectors to values
        """
        browser = ctx.request_context.lifespan_context["browser"]
        results = []
        
        for selector, value in form_data.items():
            try:
                await browser.input(selector, value)
                results.append(f"✅ Filled {selector} with '{value}'")
            except Exception as e:
                results.append(f"❌ Failed to fill {selector}: {str(e)}")
                
        return "\n".join(results)
        
    @mcp.tool()
    async def submit_form(ctx: Context, form_selector: str = "form") -> str:
        """Submit a form
        
        Args:
            form_selector: CSS selector for the form element
        """
        browser = ctx.request_context.lifespan_context["browser"]
        await browser.js_eval(f"document.querySelector('{form_selector}').submit();")
        return f"Submitted form: {form_selector}"
