"""Progress display utilities"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()


def create_progress() -> Progress:
    """Create a rich progress bar"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )


def print_success(message: str) -> None:
    """Print success message"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message"""
    console.print(f"[red]✗[/red] {message}")


def print_warning(message: str) -> None:
    """Print warning message"""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_info(message: str) -> None:
    """Print info message"""
    console.print(f"[blue]ℹ[/blue] {message}")
