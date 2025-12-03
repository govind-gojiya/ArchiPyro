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
            "Clean Architecture",
            "MVC",
            "Minimal",
        ],
    ).ask()

def ask_database() -> str:
    return questionary.select(
        "Select database:",
        choices=[
            questionary.Choice("SQLite", "SQLite - Lightweight file-based database"),
            questionary.Choice("PostgreSQL", "PostgreSQL - Advanced open-source database"),
            questionary.Choice("MySQL", "MySQL - Popular relational database"),
            questionary.Choice("MongoDB", "MongoDB - NoSQL document database"),
        ],
    ).ask()

def ask_optional_features(architecture: str, framework: str = None, database: str = None) -> list[str]:
    """
    Ask for features based on architecture, framework, and database.
    
    Args:
        architecture: Architecture pattern (Minimal, MVC, Clean Architecture)
        framework: Framework (Flask, FastAPI) - optional, for filtering
        database: Database type (PostgreSQL, MySQL, SQLite, MongoDB) - optional, for filtering
    
    Returns:
        List of selected features
    """
    # Base feature lists
    if architecture == "Minimal":
        # Minimal architecture: very limited features
        all_features = [
            "Docker",
        ]
    
    elif architecture == "MVC":
        # MVC architecture: template-focused features
        all_features = [
            "SQLAlchemy / ORM",
            "Alembic / DB Migrations",
            "Mail Service",
            "Session-Based Auth",
            "Docker",
            "GitHub Actions CI",
            "Logging Setup",
        ]
    
    else:  # Clean Architecture
        # Clean Architecture: all features available
        all_features = [
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
        ]
    
    # Filter features based on database
    if database == "MongoDB":
        # Remove SQL-specific features for MongoDB
        all_features = [f for f in all_features if f not in ["SQLAlchemy / ORM", "Alembic / DB Migrations"]]
    
    elif database in ["PostgreSQL", "MySQL", "SQLite"]:
        # SQL databases - keep SQL features
        pass  # No filtering needed
    
    # Filter features based on framework (if needed in future)
    # Currently both Flask and FastAPI support the same features
    
    # Show filtered features to user
    return questionary.checkbox(
        "Enable optional features:",
        choices=all_features,
    ).ask() or []

