#!/usr/bin/env python3
"""
Extract all unique meeting IDs from the page_dump.html file.
- Looks for <a> tags with hrefs matching /calls/{meeting_id}
- Prints all unique meeting IDs found
"""
import re
from bs4 import BeautifulSoup

# Path to the HTML dump file
HTML_DUMP_PATH = 'page_dump.html'

# Regular expression to match meeting URLs
MEETING_URL_REGEX = re.compile(r'/calls/(\d+)')

def extract_meeting_ids(html_path):
    """
    Extracts unique meeting IDs from the given HTML file.
    Args:
        html_path (str): Path to the HTML file to parse.
    Returns:
        set: Set of unique meeting IDs as strings.
    """
    meeting_ids = set()
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        # Find all <a> tags
        for a in soup.find_all('a', href=True):
            match = MEETING_URL_REGEX.search(a['href'])
            if match:
                meeting_ids.add(match.group(1))
    return meeting_ids

def main():
    meeting_ids = extract_meeting_ids(HTML_DUMP_PATH)
    print(f"Found {len(meeting_ids)} unique meeting IDs:")
    for mid in sorted(meeting_ids):
        print(mid)

    # Save to Markdown file
    md_path = 'meeting_ids.md'
    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# Extracted Meeting IDs\n\n")
        md_file.write(f"Total: {len(meeting_ids)}\n\n")
        for mid in sorted(meeting_ids):
            md_file.write(f"- `{mid}`\n")
    print(f"Meeting IDs saved to {md_path}")

if __name__ == '__main__':
    main() 