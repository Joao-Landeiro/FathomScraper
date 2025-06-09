import argparse
import sys
import json
import asyncio
from pathlib import Path

from rich.console import Console
from rich.progress import Progress

# Local imports
from auth_module.auth import FathomAuth
from scrape import FathomScraper
from export import MarkdownExporter
from ui import display_main_menu, get_scrape_limit, display_welcome_message
from config_module import load_config, check_config_exists, create_env_file

# Initialize Rich Console
console = Console()

def get_app_state() -> dict:
    """Reads master and processed lists and returns the counts."""
    master_list_path = "meetings_master_list.json"
    processed_urls_path = "processed_urls.json"
    
    state = {'total': 0, 'scraped': 0}
    
    try:
        with open(master_list_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            state['total'] = len(data.get('meetings', []))
    except (FileNotFoundError, json.JSONDecodeError):
        pass # Keep total at 0

    try:
        with open(processed_urls_path, "r", encoding="utf-8") as f:
            processed_urls = json.load(f)
            state['scraped'] = len(processed_urls)
    except (FileNotFoundError, json.JSONDecodeError):
        pass # Keep scraped at 0
        
    return state

def run_setup_flow():
    """Orchestrates the first-time setup or reconfiguration. Returns the new config."""
    display_welcome_message()
    new_config = create_env_file()
    if new_config:
        console.print("[bold green]\nSetup complete! Continuing to the main menu...[/bold green]")
        return new_config
    else:
        console.print("[bold red]\nSetup failed or was cancelled. Exiting.[/bold red]")
        sys.exit(0)

async def run_discover_mode(scraper: FathomScraper):
    """Runs the meeting discovery process and saves new meeting data."""
    console.print("[cyan]Starting meeting discovery...[/cyan]")
    
    master_list_path = "meetings_master_list.json"
    
    try:
        with open(master_list_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            master_list = data.get('meetings', [])
            existing_ids = set(m['id'] for m in master_list)
    except (FileNotFoundError, json.JSONDecodeError):
        master_list = []
        existing_ids = set()
    
    console.print(f"Found {len(master_list)} meetings in the master list.")

    # Pass existing IDs to the discovery function
    discovered_meetings, is_full_sync = await scraper.discover_meetings(existing_ids=existing_ids)
    
    if not discovered_meetings and not is_full_sync:
        console.print("[green]✓ No new meetings found. Everything is up to date.[/green]")
        return

    if not discovered_meetings and is_full_sync:
        console.print("[yellow]No new meetings were discovered from the API.[/yellow]")
        return

    new_meetings_found = 0
    for meeting in discovered_meetings:
        if meeting['id'] not in existing_ids:
            master_list.append(meeting)
            existing_ids.add(meeting['id'])
            new_meetings_found += 1
            
    if new_meetings_found == 0:
        console.print("[green]✓ No new meetings found after full sync. Everything is up to date.[/green]")
        return

    data_to_save = {
        "encoding": "utf-8",
        "meetings": master_list
    }
    with open(master_list_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]✓ Discovery complete. Found and saved {new_meetings_found} new meetings.[/green]")

async def run_scrape_mode(scraper: FathomScraper, config: dict, limit: int = None):
    """Runs the scraping process for new meetings."""
    console.print("[cyan]Starting to scrape new meetings...[/cyan]")
    exporter = MarkdownExporter(config['output_dir'])
    master_list_path = "meetings_master_list.json"
    processed_urls_path = "processed_urls.json"

    try:
        with open(master_list_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_meetings = data.get('meetings', [])
    except (FileNotFoundError, json.JSONDecodeError):
        console.print(f"[yellow]Master list ({master_list_path}) not found or is invalid. Run discover first.[/yellow]")
        return

    try:
        with open(processed_urls_path, "r") as f:
            processed_urls = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        processed_urls = set()
    
    meetings_to_process = [m for m in all_meetings if m['source'] not in processed_urls]

    if not meetings_to_process:
        console.print("[green]No new meetings to scrape. Everything is up to date![/green]")
        return

    if limit is not None and limit > 0:
        console.print(f"[yellow]Limiting scrape to {limit} meetings.[/yellow]")
        meetings_to_process = meetings_to_process[:limit]

    console.print(f"Found {len(meetings_to_process)} new meetings to scrape.")

    with Progress() as progress:
        task = progress.add_task("[green]Scraping transcripts...", total=len(meetings_to_process))
        
        for meeting_data in meetings_to_process:
            try:
                transcript = await scraper.fetch_transcript(meeting_data['source'])
                meeting_data['transcript'] = transcript
                exporter.export_meeting(meeting_data)
                processed_urls.add(meeting_data['source'])
                progress.update(task, advance=1, description=f"Scraped: {meeting_data['title']}")

            except Exception as e:
                console.print(f"[red]Error scraping meeting {meeting_data.get('id')}: {e}[/red]")

    with open(processed_urls_path, "w") as f:
        json.dump(list(processed_urls), f, indent=2)
        
    console.print("[green]✓ Scraping complete.[/green]")


async def main():
    """Main function to run the Fathom Scraper."""
    config = load_config()

    # If config is missing or invalid, run the setup flow.
    if not config:
        display_welcome_message()
        console.print("[bold yellow]Configuration not found or invalid. Starting setup...[/bold yellow]")
        config = run_setup_flow() # This will either return a valid config or exit.

    parser = argparse.ArgumentParser(description="Scrape Fathom video transcripts.")
    parser.add_argument("--discover", action="store_true", help="Discover new meetings.")
    parser.add_argument("--scrape", action="store_true", help="Scrape new meetings.")
    parser.add_argument("--limit", type=int, help="Limit the number of meetings to scrape.")
    
    # Check if command-line arguments are provided
    if len(sys.argv) > 1:
        args = parser.parse_args()
        # Config is already loaded, so we can proceed
        
        auth = FathomAuth()
        try:
            page = await auth.get_authenticated_page(config)
            if not page:
                sys.exit(1)
            
            scraper = FathomScraper(page)
            if args.discover:
                await run_discover_mode(scraper)
            elif args.scrape:
                await run_scrape_mode(scraper, config, args.limit)
        finally:
            await auth.cleanup()

    # If no command-line arguments, show interactive menu
    else:
        # Config is already loaded, so we can proceed
        display_welcome_message()
        
        # Get the initial app state
        app_state = get_app_state()
        
        while True:
            choice = display_main_menu(
                total_meetings=app_state.get('total', 0),
                scraped_meetings=app_state.get('scraped', 0)
            )
            auth = FathomAuth()
            try:
                if choice == "1": # Discover
                    page = await auth.get_authenticated_page(config)
                    if page:
                        scraper = FathomScraper(page)
                        await run_discover_mode(scraper)
                        # Refresh the state after discovery
                        app_state = get_app_state()
                elif choice == "2": # Scrape
                    limit = get_scrape_limit()
                    page = await auth.get_authenticated_page(config)
                    if page:
                        scraper = FathomScraper(page)
                        await run_scrape_mode(scraper, config, limit)
                        # Refresh the state after scraping
                        app_state = get_app_state()
                elif choice == "3": # Setup
                    config = run_setup_flow()
                    # Refresh state in case output dir changed where processed_urls might live
                    app_state = get_app_state()
                elif choice == "4": # Exit
                    console.print("[bold cyan]Goodbye![/bold cyan]")
                    sys.exit(0)
                else:
                    console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            finally:
                await auth.cleanup()


if __name__ == "__main__":
    asyncio.run(main()) 