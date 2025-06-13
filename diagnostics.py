#!/usr/bin/env python3
"""
Diagnostics script for investigating Fathom API responses.
This is a standalone script that doesn't interfere with the main codebase.
"""
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('diagnostics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FathomDiagnostics:
    def __init__(self):
        """Initialize the diagnostics tool."""
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    async def setup(self):
        """Set up the browser environment."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
    async def cleanup(self):
        """Clean up resources."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    async def login(self) -> bool:
        """Perform login to Fathom."""
        load_dotenv('env.env')
        email = os.getenv('FATHOM_EMAIL')
        password = os.getenv('FATHOM_PASSWORD')
        
        if not email or not password:
            logger.error("Missing FATHOM_EMAIL or FATHOM_PASSWORD in env.env")
            return False
            
        try:
            logger.info("Navigating to login page...")
            await self.page.goto('https://fathom.video/users/sign_in')
            await self.page.click('button:has-text("Sign in with Google")')
            
            # Wait for Google login page
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            
            # Email
            await self.page.fill('input[type="email"]', email)
            await self.page.click('button:has-text("Next")')
            
            # Password
            await self.page.wait_for_selector('input[type="password"]', timeout=10000)
            await self.page.fill('input[type="password"]', password)
            await self.page.click('button:has-text("Next")')
            
            # Wait for successful navigation
            await self.page.wait_for_url("**/home", timeout=30000)
            logger.info("Login successful!")
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
            
    async def investigate_api(self):
        """Investigate the API responses."""
        logger.info("Starting API investigation...")
        
        # Set up response interception
        async def handle_response(response):
            if "/calls/previous" in response.url:
                logger.info(f"\n=== API Response from: {response.url} ===")
                logger.info(f"Status: {response.status}")
                
                # Log headers
                logger.info("Response Headers:")
                for key, value in response.headers.items():
                    logger.info(f"  {key}: {value}")
                
                # Log body
                try:
                    json_body = await response.json()
                    logger.info("Response Body:")
                    logger.info(json.dumps(json_body, indent=2))
                    
                    # Save to file for later analysis
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"api_response_{timestamp}.json"
                    with open(filename, 'w') as f:
                        json.dump(json_body, f, indent=2)
                    logger.info(f"Response saved to {filename}")
                    
                except Exception as e:
                    logger.error(f"Failed to parse response body: {e}")
                
                logger.info("=== End of Response ===\n")
        
        # Add response listener
        self.page.on("response", handle_response)
        
        # Navigate and scroll to trigger API calls
        logger.info("Navigating to home page...")
        await self.page.goto("https://fathom.video/home", wait_until="networkidle")
        
        # Scroll to trigger API calls
        for i in range(5):
            logger.info(f"Scrolling... (Attempt {i+1}/5)")
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await self.page.wait_for_timeout(3000)
        
        # Remove listener
        self.page.remove_listener("response", handle_response)
        logger.info("API investigation complete!")

async def main():
    """Main function to run the diagnostics."""
    diagnostics = FathomDiagnostics()
    try:
        await diagnostics.setup()
        if await diagnostics.login():
            await diagnostics.investigate_api()
    finally:
        await diagnostics.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 