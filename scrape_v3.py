#!/usr/bin/env python3
"""
Scraping functionality for Fathom video transcripts using share URLs.
Version 3: participant_id field removed from participant structure. This is because IDs are not needed in the broader data pipeline; unique IDs will be generated elsewhere. All logic and validation related to participant_id has been removed for clarity and simplicity.
"""
import asyncio
import json
import logging
import re
import random
import os
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraper_v3.log')
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

    def _parse_meeting_data_from_api_v3(self, api_item: Dict) -> Dict:
        """
        Parses a single meeting item from the API response into our enhanced format (v3).
        participant_id is omitted by design; IDs are not needed in the broader pipeline.
        Includes detailed participant information with host/guest status.
        Args:
            api_item: Raw meeting data from the API
        Returns:
            Dict containing parsed meeting data with enhanced participant structure (no participant_id)
        """
        self.logger.info(f"Parsing meeting data (v3, no participant_id) for meeting ID: {api_item.get('id')}")
        meeting_id = api_item.get('id')
        participants = []
        # Process host information
        if host := api_item.get('host'):
            host_data = {
                # 'participant_id' intentionally omitted
                'name': f"{host.get('first_name', '')} {host.get('last_name', '')}".strip(),
                'is_host': True
            }
            self.logger.debug(f"Processed host data: {host_data}")
            participants.append(host_data)
        # Process contact/guest information
        if contact := api_item.get('contact'):
            guest_data = {
                # 'participant_id' intentionally omitted
                'name': contact.get('name', ''),
                'is_host': False
            }
            self.logger.debug(f"Processed guest data: {guest_data}")
            participants.append(guest_data)
        # Validate participant data
        self._validate_participants(participants)
        parsed_data = {
            'id': meeting_id,
            'title': api_item.get('title', 'Untitled Meeting'),
            'date': api_item.get('started_at', datetime.now().isoformat()),
            'duration': f"{api_item.get('duration_minutes', 0)}m",
            'participants': participants,
            'source': f"https://fathom.video/calls/{meeting_id}",
            'transcript': ''  # This will be filled in by a separate step
        }
        self.logger.info(f"Successfully parsed meeting data for ID: {meeting_id}")
        return parsed_data

    def _validate_participants(self, participants: List[Dict]) -> None:
        """
        Validates the participant data structure (v3, no participant_id).
        Args:
            participants: List of participant dictionaries
        Raises:
            ValueError: If validation fails
        """
        self.logger.debug("Validating participant data structure (no participant_id)")
        if not participants:
            self.logger.warning("No participants found in meeting data")
            return
        # Check for exactly one host
        host_count = sum(1 for p in participants if p.get('is_host', False))
        if host_count != 1:
            self.logger.warning(f"Expected exactly one host, found {host_count}")
        # Validate each participant
        for participant in participants:
            # Check required fields
            if 'name' not in participant or not participant['name']:
                self.logger.warning(f"Participant missing name: {participant}")
            if 'is_host' not in participant:
                self.logger.warning(f"Participant missing is_host flag: {participant}")
        # Note: No participant_id validation in v3

    def _convert_to_old_format(self, meeting_data: Dict) -> Dict:
        """
        Converts the new participant format to the old format for backward compatibility.
        Args:
            meeting_data: Meeting data in new format
        Returns:
            Dict with participants in old format
        """
        self.logger.debug("Converting to old participant format")
        old_format = meeting_data.copy()
        old_format['participants'] = [p['name'] for p in meeting_data['participants']]
        return old_format

    # ... existing code for discover_meetings, fetch_transcript, etc. remains unchanged ... 