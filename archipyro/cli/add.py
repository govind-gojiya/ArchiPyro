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
    Only available for Clean Architecture.
    """
    config = get_config()
    
    # Check architecture
    if config.architecture != "Clean Architecture":
        typer.echo(f"❌ 'add service' is only available for Clean Architecture.")
        typer.echo(f"   Your project uses: {config.architecture}")
        if config.architecture == "MVC":
            typer.echo(f"   💡 Use 'archipyro add resource {name}' instead.")
        raise typer.Exit(1)
    
    if config.framework == "Flask":
        typer.echo(f"❌ 'add service' isn't used in this architecture.")
        raise typer.Exit(1)
    
    generator = Generator()
    generator.generate_service(config, name)
    typer.echo(f"✅ Added service: {name}")

@app.command()
def repository(name: str):
    """
    Add a new repository component.
    
    Automatically singularizes the name (e.g., 'users' -> 'UserRepository').
    Only available for Clean Architecture.
    """
    config = get_config()
    
    # Check architecture
    if config.architecture != "Clean Architecture":
        typer.echo(f"❌ 'add repository' is only available for Clean Architecture.")
        typer.echo(f"   Your project uses: {config.architecture}")
        if config.architecture == "MVC":
            typer.echo(f"   💡 Use 'archipyro add resource {name}' instead.")
        raise typer.Exit(1)
    
    if config.framework == "Flask":
        typer.echo(f"❌ 'add repository' isn't used in this architecture.")
        raise typer.Exit(1)
    
    generator = Generator()
    generator.generate_repository(config, name)
    typer.echo(f"✅ Added repository: {name}")

@app.command()
def model(name: str):
    """
    Add a new database model.
    
    Automatically singularizes the name (e.g., 'users' -> 'User').
    """
    config = get_config()
    generator = Generator()
    generator.generate_model(config, name)
    typer.echo(f"✅ Added model: {name}")

@app.command()
def route(name: str):
    """
    Add a new route/router.
    
    Automatically singularizes the name (e.g., 'users' -> 'user.py').
    """
    config = get_config()
    generator = Generator()
    generator.generate_route(config=config, name=name, is_resource=False)
    typer.echo(f"✅ Added route: {name}")

@app.command()
def view(name: str):
    """
    Add a new view (Business Logic).
    
    Automatically singularizes the name (e.g., 'users' -> 'user_view.py').
    Only available for Clean Architecture.
    """
    config = get_config()
    
    if config.framework != "Flask" and config.architecture != "Clean Architecture":
        typer.echo(f"❌ 'add view' is only available for Clean Architecture of Flask.")
        raise typer.Exit(1)
        
    generator = Generator()
    generator.generate_view(config=config, name=name, is_resource=False)
    typer.echo(f"✅ Added view: {name}")

@app.command()
def form(name: str):
    """
    Add a new form (Input Validation).
    
    Automatically singularizes the name (e.g., 'users' -> 'user_form.py').
    Only available for Clean Architecture.
    """
    config = get_config()
    
    if config.framework != "Flask" and config.architecture != "Clean Architecture":
        typer.echo(f"❌ 'add form' is only available for Clean Architecture of Flask.")
        raise typer.Exit(1)
        
    generator = Generator()
    generator.generate_form(config=config, name=name, is_resource=False)
    typer.echo(f"✅ Added form: {name}")

@app.command()
def middleware(name: str):
    """
    Add a new middleware.
    
    Automatically singularizes the name (e.g., 'logging' -> 'logging_middleware.py').
    """
    config = get_config()

    if config.framework != "Flask" and config.architecture != "Clean Architecture":
        typer.echo(f"❌ 'add middleware' is only available for Clean Architecture of Flask.")
        raise typer.Exit(1)
    
    generator = Generator()
    generator.generate_middleware(config, name)
    typer.echo(f"✅ Added middleware: {name}")

@app.command()
def resource(name: str):
    """
    Add a complete resource (Model + Route + Templates).
    
    For MVC: Creates model, route, and CRUD templates.
    For Clean: Creates model, repository, service, and route.
    
    Example: archipyro add resource product
    """
    config = get_config()
    generator = Generator()
    
    if config.architecture == "MVC":
        typer.echo(f"🚀 Creating MVC resource: {name}")
        # Generate model
        generator.generate_model(config, name)
        typer.echo(f"  ✅ Model created")
        
        # Generate route
        generator.generate_route(config, name)
        typer.echo(f"  ✅ Route created")
        
        # Generate templates (list, detail, form)
        generator.generate_mvc_templates(config, name)
        typer.echo(f"  ✅ Templates created")
        
        typer.echo(f"\n✅ Resource '{name}' created successfully!")
        typer.echo(f"   📁 app/models/{name.lower()}.py")
        typer.echo(f"   📁 app/routes/{name.lower()}.py")
        typer.echo(f"   📁 app/templates/{name.lower()}/")
    elif config.architecture == "Clean Architecture":
        # Clean Architecture
        typer.echo(f"🚀 Creating Clean Architecture resource: {name}")
        generator.generate_model(config, name)
        typer.echo(f"  ✅ Model created")
        
        if config.framework == "Flask":
             generator.generate_view(config=config, name=name, is_resource=True)
             typer.echo(f"  ✅ View created")
             
             generator.generate_form(config=config, name=name, is_resource=True)
             typer.echo(f"  ✅ Form created")
        else:
             generator.generate_repository(config=config, name=name, is_resource=True)
             typer.echo(f"  ✅ Repository created")
             
             generator.generate_service(config=config, name=name, is_resource=True)
             typer.echo(f"  ✅ Service created")
        
        generator.generate_route(config=config, name=name, is_resource=True)
        typer.echo(f"  ✅ Route created")
        
        typer.echo(f"\n✅ Resource '{name}' created successfully!")

        if config.framework == "Flask":
            typer.echo(f"   📁 app/models/{name.lower()}.py")
            typer.echo(f"   📁 app/views/{name.lower()}_view.py")
            typer.echo(f"   📁 app/forms/{name.lower()}_form.py")
            typer.echo(f"   📁 app/routes/{name.lower()}_route.py")
        else:
            typer.echo(f"   📁 app/models/{name.lower()}.py")
            typer.echo(f"   📁 app/repositories/{name.lower()}_repository.py")
            typer.echo(f"   📁 app/services/{name.lower()}_service.py")
            typer.echo(f"   📁 app/routes/{name.lower()}_route.py")
    else:
        typer.echo(f"❌ 'add resource' is only available for MVC or Clean Architecture.")
        raise typer.Exit(1)

@app.command()
def template(name: str):
    """
    Add a standalone HTML template.
    
    Only available for MVC architecture.
    Creates a new template file in app/templates/
    
    Example: archipyro add template about
    """
    config = get_config()
    
    if config.architecture not in ["MVC"]:
        typer.echo(f"❌ 'add template' is only available for MVC architecture.")
        typer.echo(f"   Your project uses: {config.architecture}")
        raise typer.Exit(1)
    
    generator = Generator()
    generator.generate_standalone_template(config, name)
    typer.echo(f"✅ Template created: app/templates/{name.lower()}.html")

if __name__ == "__main__":
    app()
