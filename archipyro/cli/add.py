import typer
from archipyro.core.config import ProjectConfig
from archipyro.core.generator import Generator
import sys

app = typer.Typer()

def get_config():
    try:
        return ProjectConfig.load("archipyro.json")
    except FileNotFoundError:
        typer.echo("Error: archipyro.json not found. Are you in the project root?")
        sys.exit(1)

@app.command()
def service(name: str):
    """
    Add a new service component.
    
    Automatically singularizes the name (e.g., 'users' -> 'UserService').
    """
    config = get_config()
    generator = Generator()
    generator.generate_service(config, name)
    typer.echo(f"Added service: {name}")

@app.command()
def repository(name: str):
    """
    Add a new repository component.
    
    Automatically singularizes the name (e.g., 'users' -> 'UserRepository').
    """
    config = get_config()
    generator = Generator()
    generator.generate_repository(config, name)
    typer.echo(f"Added repository: {name}")

@app.command()
def model(name: str):
    """
    Add a new database model.
    
    Automatically singularizes the name (e.g., 'users' -> 'User').
    """
    config = get_config()
    generator = Generator()
    generator.generate_model(config, name)
    typer.echo(f"Added model: {name}")

@app.command()
def route(name: str):
    """
    Add a new route/router.
    
    Automatically singularizes the name (e.g., 'users' -> 'user.py').
    """
    config = get_config()
    generator = Generator()
    generator.generate_route(config, name)
    typer.echo(f"Added route: {name}")

@app.command()
def resource(name: str):
    """
    Add a complete vertical slice (Model, Repository, Service, Route).
    
    This is the recommended way to add new features.
    Automatically singularizes the name.
    """
    config = get_config()
    generator = Generator()
    generator.generate_resource(config, name)
    typer.echo(f"Added resource: {name}")
