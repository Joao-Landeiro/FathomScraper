"""
Test script for running the full pipeline (v3) on sample meetings.
This script tests the integration between scrape_v3.py and export_v3.py.
"""
import json
import logging
from pathlib import Path
from scrape_v3 import FathomScraper
from export_v3 import MarkdownExporterV3

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='pipeline_test_v4.log'
)
logger = logging.getLogger(__name__)

def run_pipeline_test():
    """Run the full pipeline test on sample meetings."""
    # Load sample API response
    with open('api_response_20250613_113832.json', 'r') as f:
        api_data = json.load(f)
    
    # Initialize components
    scraper = FathomScraper(None)  # No page needed for API data
    exporter = MarkdownExporterV3(output_dir='./pipeline_test_output')
    
    # Process first 3 meetings
    results = []
    for i, meeting in enumerate(api_data['items'][:3]):
        logger.info(f"Processing meeting {i+1}/3")
        
        try:
            # Parse meeting data
            parsed_data = scraper._parse_meeting_data_from_api_v3(meeting)
            
            # Export to markdown
            output_path = exporter.export_meeting(parsed_data)
            
            results.append({
                'meeting_index': i,
                'original_data': meeting,
                'parsed_data': parsed_data,
                'output_path': output_path,
                'success': output_path is not None
            })
            
        except Exception as e:
            logger.error(f"Error processing meeting {i+1}: {str(e)}")
            results.append({
                'meeting_index': i,
                'error': str(e),
                'success': False
            })
    
    return results

if __name__ == '__main__':
    results = run_pipeline_test()
    
    # Print summary
    print("\nPipeline Test Results:")
    print("=====================")
    for result in results:
        status = "✅ Success" if result['success'] else "❌ Failed"
        print(f"\nMeeting {result['meeting_index'] + 1}: {status}")
        if result['success']:
            print(f"Output: {result['output_path']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}") 