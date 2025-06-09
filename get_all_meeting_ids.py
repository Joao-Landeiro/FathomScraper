#!/usr/bin/env python3
"""
Script to collect meeting IDs from the current page state.
First manually scroll to the bottom of the page to load all meetings,
then run this script to collect the IDs.
"""
import asyncio
import logging
from auth_module.auth import FathomAuth
from scrape import FathomScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    auth = None
    context = None
    page = None
    scraper = None
    try:
        # Initialize auth and get browser context and page
        auth = FathomAuth()
        result = await auth.get_authenticated_context()
        assert result is not None, "Authentication failed"
        context, page = result
        logger.info("Authentication successful!")
        assert page is not None, "Failed to get authenticated page"
        
        # Initialize scraper
        scraper = FathomScraper(page, auth)
        
        # Wait for user to scroll to the bottom
        input("Please scroll to the bottom of the page to load all meetings, then press Enter...")

        # Dump the full HTML of the page
        html_content = await scraper.page.content()
        with open("page_dump.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info("Full page HTML dumped to page_dump.html")

        # Collect meeting IDs
        meeting_ids = await scraper.get_all_meeting_ids()
        logger.info(f"Total unique meeting IDs collected: {len(meeting_ids)}")
        logger.info("Meeting IDs:")
        for mid in meeting_ids:
            logger.info(mid)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Clean up resources
        if scraper:
            await scraper.close()
        if page:
            await page.close()
        if context:
            await context.close()
        if auth:
            await auth.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 