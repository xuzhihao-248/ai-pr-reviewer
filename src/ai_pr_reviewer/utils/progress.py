"""进度显示工具"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()


def create_progress() -> Progress:
    """创建富文本进度条"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )


def print_success(message: str) -> None:
    """打印成功消息"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """打印错误消息"""
    console.print(f"[red]✗[/red] {message}")


def print_warning(message: str) -> None:
    """打印警告消息"""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_info(message: str) -> None:
    """打印信息消息"""
    console.print(f"[blue]ℹ[/blue] {message}")
