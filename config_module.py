"""
Configuration module for the Fathom Scraper.
Handles loading, creating, and validating the .env configuration file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def create_env_file() -> dict:
    """
    Guides the user through creating a .env file and saves their input.
    Returns the configuration dictionary on success, None on failure or cancellation.
    """
    console.print(
        Panel(
            "[bold yellow]Welcome to the Fathom Scraper Setup![/bold yellow]\n\n"
            "I'll help you create your `.env` configuration file.",
            title="[bold]Configuration Setup[/bold]",
            border_style="blue"
        )
    )

    # Get Fathom Email
    fathom_email = console.input("[bold]Enter your Fathom login email: [/bold]")

    # Get Fathom Password
    console.print(
        "[dim](For Google accounts, it's highly recommended to use a Google App Password instead of your main password.)[/dim]"
    )
    fathom_password = console.input("[bold]Enter your Fathom password: [/bold]")

    # Get Output Directory
    default_dir = "./fathom_notes"
    output_dir = console.input(
        f"[bold]Enter the output directory for your notes (press Enter to use default: '[cyan]{default_dir}[/cyan]'): [/bold]"
    )
    if not output_dir:
        output_dir = default_dir

    # Confirm settings with the user
    console.print("\n[bold]Please confirm your settings:[/bold]")
    settings_text = (
        f"  [cyan]Email:[/cyan] {fathom_email}\n"
        f"  [cyan]Password:[/cyan] {'*' * len(fathom_password)}\n"
        f"  [cyan]Output Dir:[/cyan] {output_dir}"
    )
    console.print(Panel(settings_text, title="[bold white]Final Configuration[/bold white]", border_style="green"))

    confirm = console.input("[bold]Is this correct? (y/n): [/bold]").lower()

    if confirm == 'y':
        try:
            config_data = {
                'FATHOM_EMAIL': fathom_email,
                'FATHOM_PASSWORD': fathom_password,
                'OUTPUT_DIR': output_dir,
                'HEADLESS': "true"
            }

            with open("env.env", "w") as f:
                for key, value in config_data.items():
                    f.write(f'{key}="{value}"\n')
            
            console.print("[green]✓ Configuration saved successfully to `env.env`![/green]")
            # Return the configuration dictionary on success
            return {
                'fathom_email': config_data['FATHOM_EMAIL'],
                'fathom_password': config_data['FATHOM_PASSWORD'],
                'output_dir': config_data['OUTPUT_DIR'],
                'headless': config_data['HEADLESS'].lower() == 'true'
            }
        except IOError as e:
            console.print(f"[red]Error: Could not write to `env.env` file: {e}[/red]")
            return None
    else:
        console.print("[yellow]Setup cancelled. Please run the setup again to configure the script.[/yellow]")
        return None

def check_config_exists() -> bool:
    """Checks if the env.env file exists in the root directory."""
    return Path("env.env").exists()

def load_config() -> dict:
    """
    Load configuration from .env file.
    
    Returns:
        dict: Configuration dictionary
    """
    load_dotenv(dotenv_path='env.env')
    
    config = {
        'fathom_email': os.getenv('FATHOM_EMAIL'),
        'fathom_password': os.getenv('FATHOM_PASSWORD'),
        'output_dir': os.getenv('OUTPUT_DIR', './fathom_notes'),
        'headless': os.getenv('HEADLESS', 'true').lower() == 'true'
    }
    
    # Validate required config
    if not config['fathom_email'] or not config['fathom_password']:
        # This error is primarily for command-line mode.
        # Interactive mode should prevent this from being an issue.
        console.print("[red]Error: FATHOM_EMAIL and FATHOM_PASSWORD must be set in .env file.[/red]")
        console.print("[yellow]Hint: Run the script without arguments to run the setup wizard.[/yellow]")
        return None
    
    return config 