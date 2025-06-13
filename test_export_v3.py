"""
Test module for export_v3.py functionality.
Focuses on testing the new participant structure handling.
"""
import unittest
from datetime import datetime, timezone
import yaml
from export_v3 import MarkdownExporterV3

class TestMarkdownExporterV3(unittest.TestCase):
    """Test cases for MarkdownExporterV3 class."""
    
    def setUp(self):
        """Set up test cases."""
        self.exporter = MarkdownExporterV3()
        
    def test_generate_frontmatter_v3_valid_participants(self):
        """Test frontmatter generation with valid participant structure."""
        meeting_data = {
            'title': 'Test Meeting',
            'date': '2024-03-20T10:00:00Z',
            'duration': '60m',
            'participants': [
                {
                    'name': 'John Doe',
                    'is_host': True
                },
                {
                    'name': 'Jane Smith',
                    'is_host': False
                }
            ],
            'source': 'Fathom',
            'transcript': 'Test transcript'
        }
        
        frontmatter = self.exporter.generate_frontmatter_v3(meeting_data)
        
        # Parse the YAML to verify structure
        yaml_content = frontmatter.strip('---\n')
        parsed = yaml.safe_load(yaml_content)
        
        # Verify participant structure
        self.assertEqual(len(parsed['participants']), 2)
        self.assertEqual(parsed['participants'][0]['name'], 'John Doe')
        self.assertTrue(parsed['participants'][0]['is_host'])
        self.assertEqual(parsed['participants'][1]['name'], 'Jane Smith')
        self.assertFalse(parsed['participants'][1]['is_host'])
        
        # Verify no participant_id field exists
        for participant in parsed['participants']:
            self.assertNotIn('participant_id', participant)
            
    def test_generate_frontmatter_v3_single_host(self):
        """Test frontmatter generation with only a host."""
        meeting_data = {
            'title': 'Solo Meeting',
            'date': '2024-03-20T10:00:00Z',
            'duration': '30m',
            'participants': [
                {
                    'name': 'John Doe',
                    'is_host': True
                }
            ],
            'source': 'Fathom',
            'transcript': 'Test transcript'
        }
        
        frontmatter = self.exporter.generate_frontmatter_v3(meeting_data)
        yaml_content = frontmatter.strip('---\n')
        parsed = yaml.safe_load(yaml_content)
        
        self.assertEqual(len(parsed['participants']), 1)
        self.assertEqual(parsed['participants'][0]['name'], 'John Doe')
        self.assertTrue(parsed['participants'][0]['is_host'])
        
    def test_generate_frontmatter_v3_invalid_participants(self):
        """Test frontmatter generation with invalid participant structure."""
        meeting_data = {
            'title': 'Invalid Meeting',
            'date': '2024-03-20T10:00:00Z',
            'duration': '60m',
            'participants': [
                {
                    'name': '',  # Invalid: empty name
                    'is_host': True
                },
                {
                    'name': 'Jane Smith',
                    'is_host': 'true'  # Invalid: string instead of boolean
                }
            ],
            'source': 'Fathom',
            'transcript': 'Test transcript'
        }
        
        frontmatter = self.exporter.generate_frontmatter_v3(meeting_data)
        yaml_content = frontmatter.strip('---\n')
        parsed = yaml.safe_load(yaml_content)
        
        # Should use empty list for invalid participants
        self.assertEqual(parsed['participants'], [])
        
    def test_generate_frontmatter_v3_missing_fields(self):
        """Test frontmatter generation with missing participant fields."""
        meeting_data = {
            'title': 'Missing Fields Meeting',
            'date': '2024-03-20T10:00:00Z',
            'duration': '60m',
            'participants': [
                {
                    'name': 'John Doe'
                    # Missing is_host field
                }
            ],
            'source': 'Fathom',
            'transcript': 'Test transcript'
        }
        
        frontmatter = self.exporter.generate_frontmatter_v3(meeting_data)
        yaml_content = frontmatter.strip('---\n')
        parsed = yaml.safe_load(yaml_content)
        
        # Should use empty list for invalid participants
        self.assertEqual(parsed['participants'], [])
        
    def test_generate_frontmatter_v3_unexpected_fields(self):
        """Test frontmatter generation with unexpected fields in participants."""
        meeting_data = {
            'title': 'Extra Fields Meeting',
            'date': '2024-03-20T10:00:00Z',
            'duration': '60m',
            'participants': [
                {
                    'name': 'John Doe',
                    'is_host': True,
                    'extra_field': 'should be ignored'
                }
            ],
            'source': 'Fathom',
            'transcript': 'Test transcript'
        }
        
        frontmatter = self.exporter.generate_frontmatter_v3(meeting_data)
        yaml_content = frontmatter.strip('---\n')
        parsed = yaml.safe_load(yaml_content)
        
        # Should still work with extra fields
        self.assertEqual(len(parsed['participants']), 1)
        self.assertEqual(parsed['participants'][0]['name'], 'John Doe')
        self.assertTrue(parsed['participants'][0]['is_host'])
        self.assertNotIn('extra_field', parsed['participants'][0])

if __name__ == '__main__':
    unittest.main() 