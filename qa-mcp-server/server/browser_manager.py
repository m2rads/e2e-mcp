from browser_use import BrowserUse
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def browser_lifespan() -> AsyncIterator[BrowserUse]:
    """Manage browser lifecycle"""
    browser = BrowserUse()
    try:
        yield browser
    finally:
        await browser.close()
