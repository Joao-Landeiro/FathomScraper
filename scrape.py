#!/usr/bin/env python3
"""
Scraping functionality for Fathom video transcripts using share URLs.
"""
import asyncio
import json
import logging
import re
import random
import os
from datetime import datetime
from typing import Dict, List, Optional, Set
import aiohttp
from bs4 import BeautifulSoup
from utils import time_and_screenshot
from auth_module import FathomAuth
from playwright.async_api import async_playwright
import pyperclip
import sys

# ANSI color codes (global)
BOLD_WHITE = '\033[1;37m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraper.log')
    ]
)

logger = logging.getLogger(__name__)

class FathomScraper:
    def __init__(self, page):
        """
        Initialize the scraper.
        
        Args:
            page: An authenticated Playwright page to use
        """
        self.page = page
        self.session = None
        self.max_retries = 3
        self.base_delay = 1  # Base delay for exponential backoff
        self.logger = logging.getLogger(__name__)
    
    async def load_processed_meetings(self) -> Set[str]:
        """Load set of already processed meeting IDs."""
        try:
            with open('processed_meetings.json', 'r') as f:
                return set(json.load(f))
        except:
            return set()
    
    async def save_processed_meetings(self, meeting_ids: Set[str]) -> None:
        """Save set of processed meeting IDs."""
        try:
            with open('processed_meetings.json', 'w') as f:
                json.dump(list(meeting_ids), f)
        except Exception as e:
            logger.error(f"Error saving processed meetings: {e}")
    
    def _parse_meeting_data_from_api(self, api_item: Dict) -> Dict:
        """Parses a single meeting item from the API response into our standard format."""
        meeting_id = api_item.get('id')
        participants = []
        if host := api_item.get('host'):
            participants.append(host.get('first_name', ''))
        if contact := api_item.get('contact'):
            if name := contact.get('name'):
                participants.append(name)

        return {
            'id': meeting_id,
            'title': api_item.get('title', 'Untitled Meeting'),
            'date': api_item.get('started_at', datetime.now().isoformat()),
            'duration': f"{api_item.get('duration_minutes', 0)}m",
            'participants': [p for p in participants if p], # Filter out empty names
            'source': f"https://fathom.video/calls/{meeting_id}",
            'transcript': '' # This will be filled in by a separate step
        }

    async def discover_meetings(self, existing_ids: Set[str] = set()) -> (List[Dict], bool):
        """
        Discovers meetings, with an optimization to stop early if no new meetings are found on the first page.
        
        Args:
            existing_ids: A set of meeting IDs that are already known.

        Returns:
            A tuple containing:
            - List[Dict]: A list of newly discovered meeting data dictionaries.
            - bool: True if a full sync was performed, False if it stopped early.
        """
        self.logger.info("Discovering meetings via API...")
        
        all_meetings = []
        next_cursor = None
        
        base_url = "https://fathom.video/calls/previous"
        
        try:
            # A single navigation to the home page is sufficient for an authenticated context.
            await self.page.goto("https://fathom.video/home", wait_until="load", timeout=60000)

            page_num = 1
            # --- First Page Check ---
            self.logger.info("Fetching first page to check for new meetings...")
            first_page_url = base_url
            first_page_response = await self.page.request.get(first_page_url)
            
            if not first_page_response.ok:
                self.logger.error(f"API request failed for the first page with status {first_page_response.status}")
                return [], True

            first_page_data = await first_page_response.json()
            
            if 'items' in first_page_data and isinstance(first_page_data['items'], list):
                first_page_meetings = [self._parse_meeting_data_from_api(item) for item in first_page_data['items']]
                
                # Check if all meetings on the first page are already known
                if all(meeting['id'] in existing_ids for meeting in first_page_meetings):
                    self.logger.info("No new meetings found on the first page. Stopping discovery early.")
                    return [], False # No new meetings, not a full sync
                
                # If we are here, there are new meetings on the first page.
                self.logger.info("New meetings found on the first page. Proceeding with full sync.")
                all_meetings.extend(first_page_meetings)
                next_cursor = first_page_data.get('next_cursor')
            else:
                self.logger.error("API response format was invalid; missing 'items' list on first page.")
                return [], True # Treat as a full sync with an error

            # --- Full Sync Pagination (if needed) ---
            while next_cursor:
                page_num += 1
                url = f"{base_url}?cursor={next_cursor}"
                self.logger.info(f"Fetching page {page_num}...")
                
                api_response = await self.page.request.get(url)

                if not api_response.ok:
                    self.logger.error(f"API request failed for page {page_num} with status {api_response.status}")
                    break
                
                data = await api_response.json()
                
                if 'items' in data and isinstance(data['items'], list):
                    all_meetings.extend([self._parse_meeting_data_from_api(item) for item in data['items']])
                    self.logger.info(f"Parsed {len(data['items'])} meetings from this page. Total: {len(all_meetings)}")
                else:
                    self.logger.error("API response format was invalid; missing 'items' list.")
                    break
                    
                next_cursor = data.get('next_cursor')
                if not next_cursor:
                    self.logger.info("No more pages found. Full discovery complete.")
                    break

                await asyncio.sleep(random.uniform(0.5, 1.5)) # Be polite to the server
                
            self.logger.info(f"Discovered a total of {len(all_meetings)} meetings during sync.")
            return all_meetings, True

        except Exception as e:
            self.logger.error(f"An error occurred during API meeting discovery: {e}", exc_info=True)
            return [], True

    async def fetch_transcript(self, meeting_url: str) -> str:
        """
        Fetches the transcript from a given meeting page by clicking the
        'Copy Transcript' button and retrieving it from the clipboard.

        Args:
            meeting_url: The URL of the meeting to fetch the transcript from.

        Returns:
            str: The formatted transcript text, or an error message if it fails.
        """
        self.logger.info(f"Fetching transcript for: {meeting_url}")
        try:
            # Step 1: Navigate to the meeting page
            await self.page.goto(meeting_url, wait_until="networkidle")
            await self.page.wait_for_selector('main', timeout=20000)
            self.logger.info("Page loaded. Looking for transcript controls.")

            # Step 2: Attempt to click a 'Transcript' tab to ensure content is visible.
            try:
                # This selector targets a button with the exact text "Transcript"
                transcript_tab_selector = 'button:has-text("Transcript")'
                transcript_tab = self.page.locator(transcript_tab_selector).first
                await transcript_tab.click(timeout=5000)
                self.logger.info("Clicked on the 'Transcript' tab.")
                # Wait for a moment for any dynamic content to load after the click
                await self.page.wait_for_timeout(2000)
            except Exception:
                self.logger.info("'Transcript' tab not found or not required. Assuming transcript content is already visible.")

            # Step 3: Find and click the "Copy Transcript" button.
            # We'll try a few common selectors to make this more robust.
            copy_button_selectors = [
                'button:has-text("Copy Transcript")',
                'button[aria-label*="Copy transcript" i]',
            ]

            copy_button_found = False
            for selector in copy_button_selectors:
                try:
                    button_to_click = self.page.locator(selector).first
                    # Wait for the button to be visible and enabled before clicking
                    await button_to_click.wait_for(state="visible", timeout=1500)
                    await button_to_click.click()
                    self.logger.info(f"Successfully clicked 'Copy Transcript' button using selector: {selector}")
                    copy_button_found = True
                    break  # Exit loop on success
                except Exception:
                    self.logger.debug(f"Selector '{selector}' failed, trying next one.")
                    continue  # Try the next selector

            if not copy_button_found:
                self.logger.error(f"Could not find or click the 'Copy Transcript' button for {meeting_url}.")
                await self.page.screenshot(path="debug_screenshots/copy_button_not_found.png")
                return "Transcript extraction failed: Could not find copy button."

            # Step 4: Wait for the transcript to populate the clipboard.
            await asyncio.sleep(3)

            # Step 5: Retrieve text from clipboard using pyperclip.
            transcript_text = pyperclip.paste()

            if not transcript_text or len(transcript_text.strip()) == 0:
                self.logger.warning(f"Clipboard was empty after trying to copy transcript for {meeting_url}")
                return "Transcript extraction failed: Clipboard was empty."

            self.logger.info(f"Successfully retrieved {len(transcript_text)} characters from clipboard.")
            return transcript_text.strip()

        except Exception as e:
            self.logger.error(f"An unexpected error occurred while fetching transcript for {meeting_url}: {e}", exc_info=True)
            # Take a screenshot to help with debugging any failures
            filename_slug = re.sub(r'[\\/*?:"<>|]', "", meeting_url.replace("https://", "").replace("/", "_"))
            await self.page.screenshot(path=f"debug_screenshots/error_{filename_slug}.png")
            return "Transcript extraction failed."

    async def detailed_network_investigation(self) -> None:
        """
        Performs a deep network investigation, logging full request and response data
        for any call containing '/calls/previous' to understand the pagination mechanism.
        """
        self.logger.info("--- Starting Detailed Network Investigation ---")
        self.logger.info("This will capture full request/response data for the meeting API.")

        async def handle_response(response):
            if "/calls/previous" in response.url:
                self.logger.info(f"\n--- Intercepted API Response from: {response.url} ---")
                self.logger.info(f"Status: {response.status}")
                self.logger.info("Response Headers:")
                for key, value in response.headers.items():
                    self.logger.info(f"  {key}: {value}")
                try:
                    json_body = await response.json()
                    self.logger.info("Response JSON Body:")
                    self.logger.info(json.dumps(json_body, indent=2))
                except Exception:
                    self.logger.warning("Could not parse response body as JSON.")
                self.logger.info("--- End of Intercepted Response ---")

        self.page.on("response", handle_response)

        self.logger.info("Navigating to home page and scrolling to trigger API calls...")
        await self.page.goto("https://fathom.video/home", wait_until="networkidle")

        # Scroll down to ensure we trigger any and all relevant API calls
        for i in range(5):
            self.logger.info(f"Scrolling... (Attempt {i+1}/5)")
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await self.page.wait_for_timeout(3000)

        self.page.remove_listener("response", handle_response)
        self.logger.info("\n--- Detailed Network Investigation Complete ---")

    async def close(self):
        """Clean up resources."""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_all_meeting_ids(self) -> List[str]:
        """
        Scrolls the page to the bottom, loading all meetings, and returns all unique meeting IDs.
        Uses multiple selector strategies to ensure we catch all meeting links.
        """
        logger.info("Starting to scroll and collect all meeting IDs...")
        await self.page.reload()
        await self.page.wait_for_selector('main', timeout=30000)
        await self.page.wait_for_load_state('networkidle')
        await self.page.wait_for_timeout(2000)

        # Try multiple selectors that might contain meeting links
        selectors = [
            'a[href*="/calls/"]',  # Any link containing /calls/
            'a.border-gray-800.cursor-pointer',  # Original selector
            'call-gallery a',  # Links within call-gallery
            'page-completed-calls a'  # Links within page-completed-calls
        ]

        last_height = 0
        scroll_attempts = 0
        max_attempts = 50  # Increased max attempts
        scroll_pause = 1000  # Increased pause time
        meeting_ids = set()  # Use set to ensure uniqueness

        while scroll_attempts < max_attempts:
            # Try each selector
            for selector in selectors:
                try:
                    links = await self.page.query_selector_all(selector)
                    for link in links:
                        href = await link.get_attribute('href')
                        if href:
                            match = re.search(r'/calls/(\d+)', href)
                            if match:
                                meeting_ids.add(match.group(1))
                except Exception as e:
                    logger.warning(f"Error with selector {selector}: {e}")

            # Scroll to bottom
            current_height = await self.page.evaluate('document.documentElement.scrollHeight')
            if current_height == last_height:
                scroll_attempts += 1
                if scroll_attempts >= 3:  # If height hasn't changed for 3 attempts, we're probably at the bottom
                    break
            else:
                scroll_attempts = 0
                last_height = current_height

            await self.page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await self.page.wait_for_timeout(scroll_pause)

            # Log progress
            logger.info(f"Found {len(meeting_ids)} unique meeting IDs so far...")

        # Final check for any remaining links
        for selector in selectors:
            try:
                links = await self.page.query_selector_all(selector)
                for link in links:
                    href = await link.get_attribute('href')
                    if href:
                        match = re.search(r'/calls/(\d+)', href)
                        if match:
                            meeting_ids.add(match.group(1))
            except Exception as e:
                logger.warning(f"Error in final check with selector {selector}: {e}")

        meeting_ids_list = list(meeting_ids)
        logger.info(f"Total unique meeting IDs found: {len(meeting_ids_list)}")
        return meeting_ids_list

    async def collect_current_meeting_ids(self) -> List[str]:
        """Collect meeting IDs from the current page."""
        # Find all <a> tags with the class 'border-gray-800 cursor-pointer'
        links = await self.page.query_selector_all('a.border-gray-800.cursor-pointer')
        meeting_ids = []
        for link in links:
            href = await link.get_attribute('href')
            if href:
                match = re.search(r'/calls/(\d+)', href)
                if match:
                    meeting_id = match.group(1)
                    meeting_ids.append(meeting_id)
                    logger.info(f"Found meeting ID: {meeting_id}")
                else:
                    logger.warning(f"Link href did not match expected format: {href}")
            else:
                logger.warning("Link has no href attribute")
        return meeting_ids 

    async def process_urls_from_file(self, batch_size: int = 10):
        """
        Process URLs from urls.md file in batches.
        
        Args:
            batch_size: Number of URLs to process before saving progress
        """
        # Read URLs from file
        with open('urls.md', 'r') as f:
            urls = [line.strip() for line in f if line.startswith('https://')]
        
        logger.info(f"Read {len(urls)} URLs from urls.md")
        
        # Load already processed meetings
        processed = await self.load_processed_meetings()
        
        # Create transcripts directory if it doesn't exist
        os.makedirs('transcripts', exist_ok=True)
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            for url in batch:
                meeting_id = url.split('/')[-1]
                
                # Skip if already processed
                if meeting_id in processed:
                    logger.info(f"Skipping already processed meeting: {meeting_id}")
                    continue
                    
                try:
                    logger.info(f"Processing meeting: {meeting_id}")
                    # Use existing extract_meeting_data method
                    data = await self.extract_meeting_data(url)
                    
                    if data:
                        # Save transcript
                        transcript_path = f'transcripts/{meeting_id}.txt'
                        with open(transcript_path, 'w') as f:
                            f.write(data['transcript'])
                        logger.info(f"Saved transcript to {transcript_path}")
                        
                        # Save metadata
                        metadata_path = f'transcripts/{meeting_id}_metadata.json'
                        with open(metadata_path, 'w') as f:
                            json.dump(data['metadata'], f, indent=2)
                        logger.info(f"Saved metadata to {metadata_path}")
                        
                        # Mark as processed
                        processed.add(meeting_id)
                        
                    # Add delay between requests
                    delay = random.uniform(2, 4)
                    logger.info(f"Waiting {delay:.2f} seconds before next request...")
                    await asyncio.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"Error processing {url}: {e}")
                    continue
            
            # Save progress after each batch
            await self.save_processed_meetings(processed)
            logger.info(f"Completed batch {i//batch_size + 1}. Processed {len(processed)} meetings so far.") 