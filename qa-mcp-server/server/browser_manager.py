from browser_use import Agent, Browser, BrowserConfig
from contextlib import asynccontextmanager
from typing import AsyncIterator
import os

@asynccontextmanager
async def browser_lifespan() -> AsyncIterator[Agent]:
    """Manage browser lifecycle"""
    # Configure browser
    browser_config = BrowserConfig(
        # Use appropriate path for Chrome/Chromium
        # For macOS:
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        # For Windows:
        # chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
    
    browser = Browser(config=browser_config)
    
    # Create an agent without an LLM - we'll handle the AI part through MCP
    agent = Agent(
        task="E2E Testing agent ready to perform web testing tasks",
        browser=browser,
        # We won't provide an LLM here since we're using MCP
    )
    
    try:
        yield agent
    finally:
        # Close browser when done
        await browser.close()
