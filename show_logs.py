import glob
import os
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

console = Console()


def run_tests():
    console.print(Rule("[bold blue]Running Test Suite[/bold blue]"))
    subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        check=False,
    )


def show_latest_log():
    log_files = sorted(glob.glob("logs/test_run_*.log"))
    if not log_files:
        console.print("[red]No log files found in logs/[/red]")
        return

    latest = log_files[-1]
    console.print(Rule(f"[bold green]Log file: {os.path.basename(latest)}[/bold green]"))

    with open(latest, encoding="utf-8") as f:
        lines = f.readlines()

    output = Text()
    for line in lines:
        if "[ERROR]" in line:
            output.append(line, style="bold red")
        elif "[WARNING]" in line:
            output.append(line, style="bold yellow")
        elif "PASSED" in line:
            output.append(line, style="green")
        elif "START" in line:
            output.append(line, style="cyan")
        else:
            output.append(line, style="white")

    console.print(Panel(output, title="[bold]Test Run Logs[/bold]", border_style="blue"))


if __name__ == "__main__":
    run_tests()
    console.print()
    show_latest_log()
