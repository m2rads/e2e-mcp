import os
import sys

# Set environment variables
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["BROWSER_USE_TELEMETRY_ENABLED"] = "false"
os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
os.environ["LOGLEVEL"] = "ERROR"

# Monkey-patch stdout/stderr for specific modules only
import builtins
original_print = builtins.print

def filtered_print(*args, **kwargs):
    # Ignore specific logging messages
    message = " ".join(str(arg) for arg in args)
    if "INFO" in message and "browser_use" in message:
        return
    if "WARNING" in message and "browser_use" in message:
        return
    original_print(*args, **kwargs)

builtins.print = filtered_print

# Now run mcp
os.system("mcp dev main.py")
