"""
Export module for generating Obsidian-ready Markdown files.
Handles YAML frontmatter generation and file writing.
Version 3: Updated to handle new participant structure without participant_id.
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timezone
import yaml
import logging

logger = logging.getLogger(__name__)

class MarkdownExporterV3:
    """Handles export of meeting data to Obsidian-ready Markdown files with new participant structure."""
    
    def __init__(self, output_dir: str = "./fathom_notes"):
        """
        Initialize exporter with output directory.
        
        Args:
            output_dir: Directory to save Markdown files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_frontmatter_v3(self, meeting_data: Dict) -> str:
        """
        Generate YAML frontmatter block for the meeting using the new participant structure.
        
        Args:
            meeting_data: Meeting data dictionary with new participant structure
                Expected format for participants:
                [
                    {
                        "name": "John Doe",
                        "is_host": true
                    },
                    {
                        "name": "Jane Smith",
                        "is_host": false
                    }
                ]
            
        Returns:
            str: YAML frontmatter as string
        """
        # Create a copy of meeting data to avoid modifying the original
        meeting_data = meeting_data.copy()
        
        # Validate and clean participant structure
        if not self._validate_participants_v3(meeting_data.get('participants', [])):
            logger.warning("Invalid participant structure detected. Using empty list.")
            meeting_data['participants'] = []
        else:
            # Clean participants by keeping only expected fields
            meeting_data['participants'] = [
                {
                    'name': p['name'],
                    'is_host': p['is_host']
                }
                for p in meeting_data['participants']
            ]

        # Date is already in ISO 8601 format from the API
        iso_date = meeting_data.get('date', datetime.now().isoformat())

        frontmatter_data = {
            'title': meeting_data.get('title', 'Untitled Meeting'),
            'date': iso_date,
            'duration': meeting_data.get('duration', 'N/A'),
            'participants': meeting_data.get('participants', []),
            'source': meeting_data.get('source', 'N/A'),
            'encoding': 'utf-8',
            'scrapingdate': datetime.now(timezone.utc).isoformat()
        }
        
        # Use safe_dump for clean output and to avoid execution tags
        yaml_str = yaml.safe_dump(frontmatter_data, sort_keys=False, allow_unicode=True)
        
        return f"---\n{yaml_str}---\n"

    def _validate_participants_v3(self, participants: List[Dict]) -> bool:
        """
        Validate that participants follow the new structure (without participant_id).
        
        Args:
            participants: List of participant dictionaries
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(participants, list):
            logger.error("Participants must be a list")
            return False
            
        for participant in participants:
            if not isinstance(participant, dict):
                logger.error(f"Invalid participant type: {type(participant)}")
                return False
                
            if 'name' not in participant or not participant['name']:
                logger.error("Participant missing required 'name' field")
                return False
                
            if 'is_host' not in participant:
                logger.error("Participant missing required 'is_host' field")
                return False
                
            if not isinstance(participant['is_host'], bool):
                logger.error(f"is_host must be boolean, got {type(participant['is_host'])}")
                return False
                
            # Check for unexpected fields
            expected_fields = {'name', 'is_host'}
            unexpected_fields = set(participant.keys()) - expected_fields
            if unexpected_fields:
                logger.warning(f"Unexpected fields in participant: {unexpected_fields}")
                
        return True

    def export_meeting(self, meeting_data: Dict) -> Optional[str]:
        """
        Export single meeting to Markdown file.
        
        Args:
            meeting_data: Meeting data dictionary
            
        Returns:
            str: Path to created file, or None if failed
        """
        if not self.validate_meeting_data(meeting_data):
            logger.error(f"Skipping export for meeting due to invalid data: {meeting_data.get('title')}")
            return None

        filename = self.generate_filename(meeting_data)
        frontmatter = self.generate_frontmatter_v3(meeting_data)
        transcript = self.format_transcript(meeting_data.get('transcript', ''))
        
        full_content = f"{frontmatter}\n{transcript}"
        
        filepath = self.output_dir / filename
        unique_filepath = self.handle_duplicate_filename(filepath)
        
        try:
            with open(unique_filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            logger.info(f"Successfully exported meeting to: {unique_filepath}")
            return str(unique_filepath)
        except IOError as e:
            logger.error(f"Failed to write to file {unique_filepath}: {e}")
            return None
    
    def generate_filename(self, meeting_data: Dict) -> str:
        """
        Generate filename following template: YYYY-MM-DD-<other>-<slug-title>.md
        
        Args:
            meeting_data: Meeting data dictionary
            
        Returns:
            str: Generated filename
        """
        # Parse date from ISO 8601 format, default to today if parsing fails
        try:
            date_obj = datetime.fromisoformat(meeting_data.get('date', '').replace('Z', '+00:00'))
            date_str = date_obj.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            date_str = datetime.now().strftime('%Y-%m-%d')

        # Get "other" participant, using a simpler slug
        participants = meeting_data.get('participants', [])
        other_person_slug = 'unknown-participant'
        if len(participants) > 1:
            # Assumes the second participant is the guest
            other_person_slug = self.create_slug(participants[1])
        elif participants:
             other_person_slug = self.create_slug(participants[0])

        # Create slug from title
        title_slug = self.create_slug(meeting_data.get('title', ''))

        return f"{date_str}-{other_person_slug}-{title_slug}.md"
    
    def create_slug(self, text: str) -> str:
        """
        Create URL-friendly slug from a string.
        
        Args:
            text: Input string
            
        Returns:
            str: URL-friendly slug
        """
        if not text or text.strip() == "":
            return "untitled"
        
        # Convert to lowercase, remove non-alphanumeric chars, and replace spaces with hyphens
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        return slug if slug else "untitled"
    
    def format_transcript(self, transcript: str) -> str:
        """
        Ensures transcript is clean and ready for Markdown.
        
        Args:
            transcript: Raw transcript text
            
        Returns:
            str: Formatted transcript
        """
        # The transcript from scrape.py is already well-formatted.
        # This function can be extended for more complex cleaning later.
        return transcript.strip()
    
    def handle_duplicate_filename(self, filepath: Path) -> Path:
        """
        Handle duplicate filenames by adding incremental suffix.
        
        Args:
            filepath: Original file path
            
        Returns:
            Path: Unique file path
        """
        if not filepath.exists():
            return filepath
        
        base = filepath.stem
        suffix = filepath.suffix
        parent = filepath.parent
        counter = 1
        
        while True:
            new_name = f"{base}-{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def validate_meeting_data(self, meeting_data: Dict) -> bool:
        """
        Validate that meeting data contains required fields.
        
        Args:
            meeting_data: Meeting data dictionary
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['title', 'date', 'duration', 'participants', 'transcript', 'source']
        
        for field in required_fields:
            if field not in meeting_data or not meeting_data[field]:
                logger.warning(f"Validation failed: Missing or empty required field '{field}' in meeting data.")
                return False
        
        return True 