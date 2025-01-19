import os
import sys
import time
from art import text2art
from discord import Bot
from rich.live import Live
from rich.panel import Panel
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn

from core import settings

console = Console(color_system="standard")

class ProjectType(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_logging(self):
        console.print(Panel(
            text2art(settings.bot.LOAD_TITLE, font="small"),
            border_style="dim",
            expand=False
        ))
        time.sleep(1)
        self.load_bot_functions()

    def load_bot_functions(self):
        folder_path = "cogs"
        if not os.path.exists(folder_path):
            console.print(f"[bold red]Ошибка: папка {folder_path} отсутствует в проекте.[/bold red]")
            return

        cogs = [
            f for f in os.listdir(folder_path) if f.endswith(".py") and f != "__init__.py"
        ]
        
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=False
        )

        with Live(progress, refresh_per_second=4) as live:
            task = progress.add_task(f"Загрузка винтиков...", total=len(cogs))
            for cog in cogs:
                cog_name = cog[:-3]
                try:
                    self.load_extension(f"{folder_path}.{cog_name}")
                    progress.update(task, advance=1, description=f"Loading {cog_name}")
                    time.sleep(0.2)
                except Exception as e:
                    console.print(f"\n[red]Ошибка загрузки {cog_name}: {str(e)}[/red]")
                    sys.exit(1)

            progress.update(task, description=f"[green]Винтики подгрузились[/green]")
            time.sleep(0.5)

    def run(self, token):
        os.system("cls" if os.name == 'nt' else 'clear')
        self.setup_logging()
        super().run(token)