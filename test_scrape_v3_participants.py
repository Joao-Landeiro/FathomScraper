import json
from scrape_v3 import FathomScraper

# Load a sample API response
with open('api_response_20250613_113832.json', 'r') as f:
    api_data = json.load(f)

# Simulate a Playwright page (not needed for this test)
dummy_page = None
scraper = FathomScraper(dummy_page)

# Pick a single meeting item to test
# (Adjust the key if your JSON structure is different)
sample_meeting = api_data['items'][0]

# Parse using the new v3 method
parsed = scraper._parse_meeting_data_from_api_v3(sample_meeting)

# Print the result
print(json.dumps(parsed['participants'], indent=2, ensure_ascii=False)) 