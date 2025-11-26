import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

def print_welcome():
    console.print(Panel.fit("[bold cyan]ArchiPyro[/bold cyan]\nForge scalable Python backend architectures in seconds.", border_style="cyan"))

def ask_project_name(default: str = "my_project") -> str:
    return questionary.text("Project name:", default=default).ask()

def ask_framework() -> str:
    return questionary.select(
        "Select framework:",
        choices=["Flask", "FastAPI"],
    ).ask()

def ask_architecture() -> str:
    return questionary.select(
        "Select architecture pattern:",
        choices=[
            "Clean Architecture (Services + Repositories + Domain)",
            "MVC",
            "Minimal",
        ],
    ).ask()

def ask_database() -> str:
    return questionary.select(
        "Select database:",
        choices=[
            "SQLite",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "None",
        ],
    ).ask()

def ask_optional_features(architecture: str) -> list[str]:
    """Ask for features based on architecture."""
    
    if architecture == "Minimal":
        # Minimal architecture: very limited features
        return questionary.checkbox(
            "Enable optional features:",
            choices=[
                "Docker",
            ],
        ).ask() or []
    
    elif architecture == "MVC":
        # MVC architecture: template-focused features
        return questionary.checkbox(
            "Enable optional features:",
            choices=[
                "SQLAlchemy / ORM",
                "Alembic / DB Migrations",
                "Mail Service",
                "Session-Based Auth",
                "Docker",
                "GitHub Actions CI",
                "Logging Setup",
            ],
        ).ask() or []
    
    else:  # Clean Architecture
        # Clean Architecture: all features available
        return questionary.checkbox(
            "Enable optional features:",
            choices=[
                "SQLAlchemy / ORM",
                "Alembic / DB Migrations",
                "Redis / Cache",
                "Celery / RQ Background Tasks",
                "Mail Service",
                "JWT / Auth Template",
                "Docker",
                "GitHub Actions CI",
                "Pre-configured Tests (pytest)",
                "Logging Setup",
            ],
        ).ask() or []

