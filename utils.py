import asyncio
import functools
import logging
import time
from pathlib import Path
from typing import Callable, Any
import subprocess
import sys

logger = logging.getLogger(__name__)

def check_and_install_playwright_browsers():
    """
    Checks if Playwright browsers are installed and installs them if they are not,
    by programmatically invoking the Playwright CLI. This is the standard way
    to ensure browsers are available for a packaged application.
    """
    print("Checking for required browser binaries...")
    print("This may take a few minutes on the first run, please be patient...")
    try:
        # We run the 'install' command via a subprocess. Playwright's CLI is idempotent
        # and will only download what's missing.
        # We specify 'chromium' to only install what we need.
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("Browser check/installation complete.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("ERROR: Failed to automatically install browser binaries.")
        print("This can happen if you are offline or have network issues.")
        print(f"Error details: {e}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        sys.exit(1)

def ensure_screenshots_dir():
    """Ensure the screenshots directory exists."""
    screenshots_dir = Path("debug_screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    return screenshots_dir

def time_and_screenshot(page, operation_name: str, threshold_ms: int = 1000) -> Callable:
    """
    Decorator factory that times an async operation and takes a screenshot if it exceeds the threshold.
    
    Args:
        page: Playwright page object
        operation_name: Name of the operation for logging and screenshot filename
        threshold_ms: Time threshold in milliseconds before taking a screenshot
    """
    screenshots_dir = ensure_screenshots_dir()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                if duration_ms > threshold_ms:
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    screenshot_path = screenshots_dir / f"{operation_name}_{timestamp}.png"
                    
                    try:
                        await page.screenshot(path=str(screenshot_path))
                        logger.info(f"Screenshot saved to {screenshot_path}")
                    except Exception as e:
                        logger.error(f"Failed to take screenshot: {e}")
                
                return result
                
            except Exception as e:
                # On error, always take a screenshot regardless of timing
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                screenshot_path = screenshots_dir / f"{operation_name}_error_{timestamp}.png"
                
                try:
                    await page.screenshot(path=str(screenshot_path))
                    logger.info(f"Error screenshot saved to {screenshot_path}")
                except Exception as screenshot_error:
                    logger.error(f"Failed to take error screenshot: {screenshot_error}")
                
                raise e
            
        return wrapper
    return decorator 