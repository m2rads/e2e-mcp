#  MCP Server for Running E2E Tests 

You can add this MCP to your Cursor or Windsurf AI IDE and improve your "Vibe Coding" workflow 

## What is MCP? 

The Model Context Protocol (MCP) is an open protocol that connects your AI agent to the source of your system or data reducing the friction between context and the AI.


## Prerequisite 

- Python 3.11 or higher
- LLM Provide (In this example I used OpenAI - You can use any AI you prefer)

## Run 

1. Setup your dev env: 
```bash
uv venv
source .venv/bin/activate
```

2. Install required packages: 
```bash
uv pip install -r requirements.txt
playwright install 
```

3. Add your LLM API Key 
```
OPENAI_API_KEY=your_openai_api_key_here
```


## Note

Since we're using stdio as MCP transport, we have disable all output from browser use

## Debugging

You can run the MCP inspector tool with this command

```bash
uv run mcp dev server.py
```