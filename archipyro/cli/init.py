import typer
from archipyro.utils import prompt
from archipyro.core.config import ProjectConfig
from rich.console import Console

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def main():
    """
    Initialize a new ArchiPyro project.
    
    Starts an interactive wizard to configure your project:
    - Framework (Flask/FastAPI)
    - Architecture (Clean/MVC)
    - Database (PostgreSQL/MySQL/SQLite/MongoDB)
    - Optional Features (Auth, Docker, CI, etc.)
    """
    prompt.print_welcome()
    
    project_name = prompt.ask_project_name()
    framework = prompt.ask_framework()
    architecture = prompt.ask_architecture()
    database = prompt.ask_database()
    features = prompt.ask_optional_features(architecture)  # Pass architecture

    
    config = ProjectConfig(
        name=project_name,
        framework=framework,
        architecture=architecture,
        database=database,
        features=features
    )
    
    console.print(f"\n[bold green]Generating project: {config.name}[/bold green]")
    console.print(f"Framework: {config.framework}")
    console.print(f"Architecture: {config.architecture}")
    console.print(f"Database: {config.database}")
    console.print(f"Features: {', '.join(config.features)}")
    
    # Call generator
    from archipyro.core.generator import Generator
    generator = Generator()
    generator.generate_project(config)
    
    console.print("\n[bold blue]Done![/bold blue]")

if __name__ == "__main__":
    app()
