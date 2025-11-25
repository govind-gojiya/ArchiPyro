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
def docker():
    """
    Generate Dockerfile and docker-compose.yml.
    
    Respects your selected database and features.
    """
    config = get_config()
    generator = Generator()
    generator.generate_docker(config)
    typer.echo("Generated Docker configuration.")

@app.command()
def ci():
    """
    Generate GitHub Actions CI/CD workflows.
    
    Creates .github/workflows/ci.yml.
    """
    config = get_config()
    generator = Generator()
    generator.generate_ci(config)
    typer.echo("Generated CI/CD workflows.")
