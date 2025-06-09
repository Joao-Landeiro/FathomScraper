import asyncio
import functools
import logging
import time
from pathlib import Path
from typing import Callable, Any

logger = logging.getLogger(__name__)

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