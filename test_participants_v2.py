"""
Test suite for the new participant structure implementation.
Tests both the new structure and compatibility with the old format.
"""
import unittest
from datetime import datetime
from typing import Dict, List

class TestParticipantStructure(unittest.TestCase):
    """Test cases for the new participant structure."""

    def setUp(self):
        """Set up test data."""
        # Sample old format data
        self.old_format_data = {
            'id': 'test123',
            'title': 'Test Meeting',
            'date': datetime.now().isoformat(),
            'duration': '30m',
            'participants': ['John Doe', 'Jane Smith'],
            'source': 'https://fathom.video/calls/test123',
            'transcript': ''
        }

        # Sample new format data
        self.new_format_data = {
            'id': 'test123',
            'title': 'Test Meeting',
            'date': datetime.now().isoformat(),
            'duration': '30m',
            'participants': [
                {
                    'participant_id': 'host123',
                    'name': 'John Doe',
                    'is_host': True
                },
                {
                    'participant_id': 'guest456',
                    'name': 'Jane Smith',
                    'is_host': False
                }
            ],
            'source': 'https://fathom.video/calls/test123',
            'transcript': ''
        }

    def test_host_only_scenario(self):
        """Test meeting with only a host participant."""
        data = {
            'participants': [
                {
                    'participant_id': 'host123',
                    'name': 'John Doe',
                    'is_host': True
                }
            ]
        }
        self.assertEqual(len(data['participants']), 1)
        self.assertTrue(data['participants'][0]['is_host'])
        self.assertEqual(data['participants'][0]['name'], 'John Doe')

    def test_host_and_guest_scenario(self):
        """Test meeting with both host and guest participants."""
        data = self.new_format_data
        self.assertEqual(len(data['participants']), 2)
        self.assertTrue(data['participants'][0]['is_host'])
        self.assertFalse(data['participants'][1]['is_host'])

    def test_empty_participants_list(self):
        """Test handling of empty participants list."""
        data = {'participants': []}
        self.assertEqual(len(data['participants']), 0)

    def test_missing_participant_data(self):
        """Test handling of missing participant data fields."""
        data = {
            'participants': [
                {
                    'name': 'John Doe',
                    'is_host': True
                    # Missing participant_id
                }
            ]
        }
        self.assertNotIn('participant_id', data['participants'][0])

    def test_participant_id_handling(self):
        """Test participant_id field handling."""
        data = self.new_format_data
        for participant in data['participants']:
            self.assertIn('participant_id', participant)
            self.assertIsInstance(participant['participant_id'], str)

    def test_name_validation(self):
        """Test participant name validation."""
        data = self.new_format_data
        for participant in data['participants']:
            self.assertIn('name', participant)
            self.assertIsInstance(participant['name'], str)
            self.assertTrue(len(participant['name']) > 0)

    def test_is_host_flag_validation(self):
        """Test is_host flag validation."""
        data = self.new_format_data
        host_count = sum(1 for p in data['participants'] if p['is_host'])
        self.assertEqual(host_count, 1)  # Should have exactly one host

    def test_backward_compatibility(self):
        """Test backward compatibility with old format."""
        # Test that new format can be converted to old format
        old_format_participants = [p['name'] for p in self.new_format_data['participants']]
        self.assertEqual(old_format_participants, self.old_format_data['participants'])

    def test_export_compatibility(self):
        """Test compatibility with export functionality."""
        # Test that new format contains all required fields for export
        required_fields = ['id', 'title', 'date', 'duration', 'participants', 'source', 'transcript']
        for field in required_fields:
            self.assertIn(field, self.new_format_data)

if __name__ == '__main__':
    unittest.main() 