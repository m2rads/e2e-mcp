import logging
import os

def configure_logging():
    """Configure logging to silence browser-use logs without affecting MCP communication"""
    # Silence specific loggers that are causing problems
    for logger_name in ["browser_use", "playwright"]:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = False
        logger.setLevel(logging.CRITICAL)
    
    # Disable telemetry
    os.environ["BROWSER_USE_TELEMETRY_ENABLED"] = "false"
    os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
