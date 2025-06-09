"""
UI Module for the Fathom Scraper.
Handles all user-facing interactive elements, like menus and welcome messages.
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn
from rich.table import Table

console = Console()

def display_welcome_message():
    """Displays a stylized welcome message for the application."""
    
    welcome_text = Text.from_markup(
        "[bold cyan]Fathom to Markdown Scraper[/bold cyan]\n\n"
        "This tool automates backing up your Fathom meeting transcripts to clean Markdown files."
    )
    
    panel = Panel(
        welcome_text,
        title="[bold white]Welcome[/bold white]",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(panel)

def display_main_menu(total_meetings: int = 0, scraped_meetings: int = 0) -> str:
    """
    Displays the main menu and prompts the user for a choice.
    Returns the user's choice as a string.
    """
    console.print("\n" + "="*50)
    
    # Create a layout table for the status
    status_grid = Table.grid(expand=True)
    status_grid.add_column(ratio=1)
    status_grid.add_column(ratio=2)
    
    status_text = f"[bold yellow]{scraped_meetings} of {total_meetings}[/bold yellow] meetings scraped"
    
    # Create a Progress instance and add a task to make it renderable
    progress = Progress(BarColumn(bar_width=None))
    progress.add_task(
        "progress", # Description is not shown, but required
        total=total_meetings or 1, # Avoid division by zero if total is 0
        completed=scraped_meetings
    )

    status_grid.add_row(status_text, progress)

    menu_text = (
        "\n[bold]Main Menu[/bold]\n\n"
        "  [cyan]1.[/cyan] [bold]Discover Meetings[/bold]\n"
        "     (Scan Fathom for new meetings and add to master list)\n\n"
        "  [cyan]2.[/cyan] [bold]Scrape New Meetings[/bold]\n"
        "     (Process meetings from the master list and create notes)\n\n"
        "  [cyan]3.[/cyan] [bold]Setup / Reconfigure[/bold]\n"
        "     (Change your email, password, or output directory)\n\n"
        "  [cyan]4.[/cyan] [bold]Exit[/bold]\n"
    )
    console.print(
        Panel(
            status_grid,
            title="[bold white]Scraping Progress[/bold white]",
            border_style="green"
        )
    )
    
    console.print(
        Panel(
            menu_text,
            title="[bold white]Select an Option[/bold white]",
            border_style="blue",
            padding=(1, 2)
        )
    )
    choice = console.input("[bold]Enter the number of your choice: [/bold]")
    return choice

def get_scrape_limit() -> int:
    """
    Prompts the user for the number of meetings to scrape.
    
    Returns:
        int: The number of meetings to scrape.
    """
    while True:
        try:
            limit_str = console.input("[bold yellow]How many meetings would you like to scrape? [/bold yellow]")
            limit = int(limit_str)
            if limit > 0:
                return limit
            else:
                console.print("[red]Please enter a positive number.[/red]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]") 