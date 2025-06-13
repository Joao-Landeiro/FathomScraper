#!/usr/bin/env python3
"""
Test script for the new participant structure implementation.
Uses real API response data to validate the implementation.
"""
import json
import logging
from scrape_v2 import FathomScraper
from playwright.async_api import async_playwright
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_implementation_v2.log')
    ]
)

logger = logging.getLogger(__name__)

async def test_with_real_data():
    """Test the new implementation with real API response data."""
    # Load API response data
    try:
        with open('api_response_20250613_113832.json', 'r') as f:
            api_data = json.load(f)
    except FileNotFoundError:
        logger.error("API response file not found")
        return

    # Initialize scraper with a dummy page (we only need the parsing functionality)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        scraper = FathomScraper(page)

        # Test parsing of each meeting in the API response
        if 'items' in api_data:
            for item in api_data['items']:
                logger.info(f"\nTesting meeting ID: {item.get('id', 'unknown')}")
                
                # Test new format parsing
                try:
                    parsed_data = scraper._parse_meeting_data_from_api_v2(item)
                    logger.info("✅ Successfully parsed with new format")
                    
                    # Validate participant structure
                    participants = parsed_data.get('participants', [])
                    logger.info(f"Found {len(participants)} participants")
                    
                    # Log participant details
                    for p in participants:
                        logger.info(f"Participant: {p.get('name')} (Host: {p.get('is_host')})")
                    
                    # Test backward compatibility
                    old_format = scraper._convert_to_old_format(parsed_data)
                    logger.info("✅ Successfully converted to old format")
                    logger.info(f"Old format participants: {old_format.get('participants')}")
                    
                except Exception as e:
                    logger.error(f"❌ Error processing meeting: {str(e)}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_with_real_data()) 