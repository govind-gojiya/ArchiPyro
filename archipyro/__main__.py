import typer
from archipyro.cli import init, add, gen

app = typer.Typer(
    name="archipyro",
    help="Forge scalable Python backend architectures in seconds.",
    add_completion=False,
)

app.add_typer(init.app, name="init", help="Initialize a new project.")
app.add_typer(add.app, name="add", help="Add components to the project.")
app.add_typer(gen.app, name="gen", help="Generate infrastructure.")

if __name__ == "__main__":
    app()
