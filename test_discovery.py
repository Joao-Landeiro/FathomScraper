#!/usr/bin/env python3
"""
Test script for meeting discovery and data extraction.
"""
import asyncio
import logging
import pytest
from auth_module.auth import FathomAuth
from scrape import FathomScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_discovery():
    """Test meeting discovery functionality."""
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
        
        # Discover meetings
        meetings = await scraper.discover_meetings()
        assert meetings is not None, "Discovery returned None"
        assert len(meetings) > 0, "No meetings found"
        
        logger.info(f"Successfully found {len(meetings)} meetings!")
        logger.info("\nFirst few meetings:")
        for i, url in enumerate(meetings[:5], 1):
            logger.info(f"{i}. {url}")
            assert url.startswith("https://fathom.video/calls/"), f"Invalid meeting URL format: {url}"
        
        # Test data extraction on first meeting
        test_url = meetings[0]
        logger.info(f"\n🔍 Testing data extraction for meeting: {test_url}")
        
        data = await scraper.extract_meeting_data(test_url)
        assert data is not None, "Failed to extract meeting data"
        
        # Verify data structure
        assert 'metadata' in data, "Missing metadata in extracted data"
        assert 'transcript' in data, "Missing transcript in extracted data"
        assert 'url' in data, "Missing URL in extracted data"
        assert 'extracted_at' in data, "Missing extraction timestamp"
        
        # Verify metadata fields
        metadata = data['metadata']
        assert 'title' in metadata, "Missing title in metadata"
        assert 'date' in metadata, "Missing date in metadata"
        assert 'duration' in metadata, "Missing duration in metadata"
        assert 'participants' in metadata, "Missing participants in metadata"
        assert 'share_url' in metadata, "Missing share URL in metadata"
        
        # Verify transcript
        assert len(data['transcript']) > 0, "Empty transcript"
        
        logger.info("Successfully verified meeting data structure!")
        logger.info("\nMetadata:")
        for key, value in data['metadata'].items():
            logger.info(f"{key}: {value}")
        logger.info(f"\nTranscript length: {len(data['transcript'])} characters")
        logger.info("First 200 characters of transcript:")
        logger.info(data['transcript'][:200] + "...")
        
        return True
        
    except AssertionError as e:
        logger.error(f"Test assertion failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        logger.exception("Detailed error:")
        return False
    finally:
        # Clean up resources
        try:
            if scraper:
                await scraper.close()
            if page:
                await page.close()
            if context:
                await context.close()
            if auth:
                await auth.cleanup()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    print("\n🔍 Testing Meeting Discovery and Data Extraction...")
    print("\n📝 This will:")
    print("1. Login to Fathom (using saved session if available)")
    print("2. Navigate to home page")
    print("3. Find all available meeting transcripts")
    print("4. Test data extraction on one meeting")
    print("5. Verify data structure and content\n")
    
    success = asyncio.run(test_discovery())
    if success:
        print("All tests passed!")
        exit(0)
    else:
        print("Tests failed!")
        exit(1) 