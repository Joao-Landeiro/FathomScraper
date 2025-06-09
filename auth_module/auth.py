"""
Authentication module for Fathom video scraping.
"""
import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Optional, List

from dotenv import load_dotenv
from playwright.async_api import async_playwright, BrowserContext, Page, Playwright

from utils import time_and_screenshot

# Load environment variables from env.env file
load_dotenv('env.env')

logger = logging.getLogger(__name__)

class FathomAuth:
    def __init__(self):
        """Initialize the auth module."""
        self.playwright: Optional[Playwright] = None
        self.browser = None
        self.context = None
        self.session_file = Path('session.json')
        
        # Common selectors for Google login elements
        self.email_input_selectors = [
            'input[type="email"]',
            'input[name="identifier"]',
            'input[name="Email"]',
            'input[name="username"]',
            'input[autocomplete="username"]',
            '#identifierId',
            '#Email',
            '#email',
            '[aria-label="Email or phone"]',
            '[aria-label="Email"]'
        ]
        
        # Success indicators for auth verification
        self.auth_success_selectors = [
            'button[aria-label="User menu"]',
            'div[role="main"]',
            'main',
            '#root',
            '.dashboard',
            'nav',
            'header'
        ]
    
    async def wait_for_any_selector(self, page: Page, selectors: List[str], timeout: int = 10000) -> str:
        """
        Wait for any of the given selectors to appear and return the first one found.
        
        Args:
            page: Playwright page object
            selectors: List of selectors to try
            timeout: Total timeout for all attempts
            
        Returns:
            str: The selector that was found
            
        Raises:
            Exception: If none of the selectors are found within the timeout
        """
        for selector in selectors:
            try:
                await page.wait_for_selector(selector, timeout=timeout / len(selectors))
                logger.info(f"Found matching selector: {selector}")
                return selector
            except Exception:
                logger.debug(f"Selector not found: {selector}")
                continue
        
        raise Exception(f"None of the selectors were found within {timeout}ms")
    
    async def wait_for_successful_navigation(self, page: Page) -> bool:
        """
        Waits for navigation to the home page and then verifies the login status.
        
        Args:
            page: Playwright page object
            
        Returns:
            bool: True if navigation and login verification were successful, False otherwise.
        """
        logger.info("Waiting for navigation to home page...")
        try:
            # Wait for the URL to contain '/home', indicating redirection is complete
            await page.wait_for_url("**/home", timeout=30000)
            logger.info("Successfully navigated to URL containing '/home'.")
            
            # Now, use our robust, patient check to verify the page has loaded
            return await self.is_logged_in(page)
            
        except Exception as e:
            logger.error(f"Failed to navigate to home page or verify login: {e}")
            await page.screenshot(path="debug_screenshots/navigation_error.png")
            return False
    
    async def is_logged_in(self, page: Page, timeout: int = 20000) -> bool:
        """
        Checks if the user is logged in by patiently waiting for a login success
        indicator to appear on the page. This is more robust for pages that
        load content dynamically.
        """
        logger.info(f"Verifying login status at {page.url} by waiting for a success selector...")
        try:
            # Use the existing helper to wait for any of the success selectors
            found_selector = await self.wait_for_any_selector(page, self.auth_success_selectors, timeout=timeout)
            logger.info(f"Login status verified. Found success selector: {found_selector}")
            return True
        except Exception:
            logger.warning("Login verification failed. Could not find any success selectors within the timeout.")
            # Taking a screenshot here is crucial for debugging why verification failed
            await page.screenshot(path="debug_screenshots/login_verification_failed.png")
            return False
    
    async def perform_fresh_login(self, page: Page) -> bool:
        """Performs a fresh login to Fathom via Google."""
        logger.info("Starting a fresh login process.")

        email = os.getenv('FATHOM_EMAIL')
        password = os.getenv('FATHOM_PASSWORD')
        if not email or not password:
            logger.error("Missing FATHOM_EMAIL or FATHOM_PASSWORD in .env file.")
            return False

        logger.info("Navigating to login page.")
        await page.goto('https://fathom.video/users/sign_in')
        await page.click('button:has-text("Sign in with Google")')
        
        # Add a wait for navigation to the Google login page to complete
        await page.wait_for_load_state("networkidle", timeout=10000)

        try:
            # Email - increase timeout to give the page more time to load
            email_selector = await self.wait_for_any_selector(page, self.email_input_selectors, timeout=15000)
            await page.fill(email_selector, email)
            await page.click('button:has-text("Next")')

            # Password
            password_selector = 'input[type="password"]'
            await page.wait_for_selector(password_selector, timeout=10000)
            await page.fill(password_selector, password)
            await page.click('button:has-text("Next")')

        except Exception as e:
            logger.error(f"Failed during Google login flow: {e}")
            await page.screenshot(path="debug_screenshots/login_error.png")
            return False

        return await self.wait_for_successful_navigation(page)

    async def get_authenticated_context(self) -> Optional[BrowserContext]:
        """
        Get authenticated context, either from session or fresh login.
        Returns the context if successful, otherwise None.
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)

        # 1. Try to use existing session file
        if self.session_file.exists():
            logger.info("Session file found. Trying to restore session.")
            try:
                storage_state = json.loads(self.session_file.read_text())
                context = await self.browser.new_context(storage_state=storage_state)
                page = await context.new_page()
                
                logger.info("Navigating to home page to verify restored session...")
                await page.goto("https://fathom.video/home", wait_until="networkidle", timeout=25000)
                
                if await self.is_logged_in(page):
                    logger.info("Session restored and verified successfully.")
                    await page.close()
                    self.context = context
                    return self.context
                else:
                    logger.warning("Session appears to be invalid. Proceeding with fresh login.")
                    # Important: close the failed context before creating a new one
                    await page.close()
                    await context.close()
            except Exception as e:
                logger.error(f"Failed to restore session: {e}. Proceeding with fresh login.")

        # 2. Perform fresh login
        logger.info("Performing a fresh login.")
        context = await self.browser.new_context()
        page = await context.new_page()
        try:
            if await self.perform_fresh_login(page):
                logger.info("Fresh login successful. Saving session state.")
                storage_state = await context.storage_state()
                self.session_file.write_text(json.dumps(storage_state))
                self.context = context
                return self.context
            else:
                logger.error("Fresh login failed.")
                await context.close()
                return None
        finally:
            if page and not page.is_closed():
                await page.close()

    async def cleanup(self):
        """Close browser and context."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def verify_auth_status(self, page: Page) -> bool:
        """Verifies authentication status on a given page."""
        return await self.is_logged_in(page)

    async def get_authenticated_page(self, config: dict) -> Optional[Page]:
        """
        High-level method to get an authenticated Playwright page.
        It relies on get_authenticated_context to handle the core logic.

        Args:
            config (dict): The application configuration dictionary.

        Returns:
            Optional[Page]: An authenticated page object, or None if authentication fails.
        """
        try:
            # get_authenticated_context now handles all verification.
            # If it returns a context, it is guaranteed to be valid.
            context = await self.get_authenticated_context()
            if context:
                logger.info("Authentication context secured. Creating new page.")
                page = await context.new_page()
                return page
            else:
                logger.error("Authentication failed, could not get context.")
                # Ensure cleanup if context fails
                await self.cleanup()
                return None
        except Exception as e:
            logger.error(f"An error occurred while getting authenticated page: {e}")
            await self.cleanup()
            return None 