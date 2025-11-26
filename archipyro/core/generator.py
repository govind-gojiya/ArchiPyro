from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import inflect
import questionary
from archipyro.core.config import ProjectConfig

class Generator:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        self.p = inflect.engine()
        
        # Register custom filters
        self.env.filters['to_pascal_case'] = self.to_pascal_case

    def to_pascal_case(self, text: str) -> str:
        """Convert snake_case to PascalCase."""
        return "".join(x.capitalize() for x in text.split("_"))

    def generate_project(self, config: ProjectConfig):
        """
        Generate a new project based on the configuration.
        """
        project_dir = Path.cwd() / config.slug
        project_dir.mkdir(exist_ok=True)
        
        # Determine template path based on framework and architecture
        arch_map = {
            "Clean Architecture": "clean",
            "MVC": "mvc",
            "Minimal": "minimal"
        }
        arch_folder = arch_map.get(config.architecture, "clean")
        template_base = f"{config.framework.lower()}/{arch_folder}"
        
        # Minimal Architecture Handling
        if config.architecture == "Minimal":
            if config.framework == "Flask":
                self._render_template(f"{template_base}/app.py.jinja2", project_dir / "app.py", config)
            else:
                self._render_template(f"{template_base}/main.py.jinja2", project_dir / "main.py", config)
            
            self._render_template(f"{template_base}/requirements.txt.jinja2", project_dir / "requirements.txt", config)
            self._render_template(f"{template_base}/README.md.jinja2", project_dir / "README.md", config)
            self._render_template("shared/.env.jinja2", project_dir / ".env", config)
            return # Stop here for Minimal

        # MVC & Clean Architecture Handling (Common steps)
        
        # Create app directory
        app_dir = project_dir / "app"
        app_dir.mkdir(exist_ok=True)
        
        # MVC Architecture Handling
        if config.architecture == "MVC":
            if config.framework == "Flask":
                # Flask MVC Structure
                self._render_template(f"{template_base}/app/__init__.py.jinja2", app_dir / "__init__.py", config)
                self._render_template(f"{template_base}/app/config.py.jinja2", app_dir / "config.py", config)
                
                # Routes
                (app_dir / "routes").mkdir(exist_ok=True)
                self._render_template(f"{template_base}/app/routes/main.py.jinja2", app_dir / "routes" / "main.py", config)
                
                # Templates and Static
                (app_dir / "templates").mkdir(exist_ok=True)
                (app_dir / "static").mkdir(exist_ok=True)
                self._render_template(f"{template_base}/app/templates/index.html.jinja2", app_dir / "templates" / "index.html", config)
                
                # Models
                (app_dir / "models").mkdir(exist_ok=True)
                (app_dir / "models" / "__init__.py").touch()
                
                # Run file
                self._render_template(f"{template_base}/run.py.jinja2", project_dir / "run.py", config)
            else:
                # FastAPI MVC Structure
                self._render_template(f"{template_base}/app/main.py.jinja2", app_dir / "main.py", config)
                
                # Routers
                (app_dir / "routers").mkdir(exist_ok=True)
                self._render_template(f"{template_base}/app/routers/main.py.jinja2", app_dir / "routers" / "main.py", config)
                (app_dir / "routers" / "__init__.py").touch()
                
                # Templates and Static
                (app_dir / "templates").mkdir(exist_ok=True)
                (app_dir / "static").mkdir(exist_ok=True)
                self._render_template(f"{template_base}/app/templates/index.html.jinja2", app_dir / "templates" / "index.html", config)
                
                # Models
                (app_dir / "models").mkdir(exist_ok=True)
                (app_dir / "models" / "__init__.py").touch()
            
            
            # Common for MVC
            self._render_template(f"{template_base}/requirements.txt.jinja2", project_dir / "requirements.txt", config)
            self._render_template(f"{template_base}/README.md.jinja2", project_dir / "README.md", config)
            self._render_template("shared/.env.jinja2", project_dir / ".env", config)
            
            # MVC Auth files (if Session-Based Auth is selected)
            if "Session-Based Auth" in config.features:
                if config.framework == "Flask":
                    # Create auth templates directory
                    (app_dir / "templates" / "auth").mkdir(exist_ok=True)
                    
                    # Create templates
                    self._render_template(f"{template_base}/app/templates/base.html.jinja2", app_dir / "templates" / "base.html", config)
                    self._render_template(f"{template_base}/app/templates/home.html.jinja2", app_dir / "templates" / "home.html", config)
                    self._render_template(f"{template_base}/app/templates/auth/login.html.jinja2", app_dir / "templates" / "auth" / "login.html", config)
                    self._render_template(f"{template_base}/app/templates/auth/register.html.jinja2", app_dir / "templates" / "auth" / "register.html", config)
                    
                    # Create User model
                    self._render_template(f"{template_base}/app/models/user.py.jinja2", app_dir / "models" / "user.py", config)
                    
                    # Create auth routes
                    self._render_template(f"{template_base}/app/routes/auth.py.jinja2", app_dir / "routes" / "auth.py", config)
            
            config.save(project_dir / "archipyro.json")
            return # Stop here for MVC

        
        # Clean Architecture Handling (existing logic)
        # Render templates
        self._render_template(f"{template_base}/requirements.txt.jinja2", project_dir / "requirements.txt", config)
        self._render_template(f"{template_base}/README.md.jinja2", project_dir / "README.md", config)
        
        self._render_template(f"{template_base}/app/__init__.py.jinja2", app_dir / "__init__.py", config)
        
        if config.framework == "Flask":
             # For Flask, main.py.jinja2 is the blueprint, goes to routes/main.py
             (app_dir / "routes").mkdir(exist_ok=True)
             self._render_template(f"{template_base}/app/main.py.jinja2", app_dir / "routes" / "main.py", config)
             
             # Celery Utils for Flask
             if "Celery / RQ Background Tasks" in config.features:
                 self._render_template(f"{template_base}/app/celery_utils.py.jinja2", app_dir / "celery_utils.py", config)

             # JWT Auth for Flask
             if "JWT / Auth Template" in config.features:
                 (app_dir / "auth").mkdir(exist_ok=True)
                 self._render_template(f"{template_base}/app/auth/utils.py.jinja2", app_dir / "auth" / "utils.py", config)
                 self._render_template(f"{template_base}/app/auth/routes.py.jinja2", app_dir / "auth" / "routes.py", config)
                 (app_dir / "auth" / "__init__.py").touch()
                 # Also need User model
                 (app_dir / "models").mkdir(exist_ok=True)
                 self._render_template(f"{template_base}/app/models/user.py.jinja2", app_dir / "models" / "user.py", config)


        else:
             # For FastAPI, main.py.jinja2 is the app entry point, goes to app/main.py
             self._render_template(f"{template_base}/app/main.py.jinja2", app_dir / "main.py", config)
             
             # FastAPI Core Config
             (app_dir / "core").mkdir(exist_ok=True)
             self._render_template(f"{template_base}/app/core/config.py.jinja2", app_dir / "core" / "config.py", config)
             (app_dir / "core" / "__init__.py").touch()

             # FastAPI Dependencies
             (app_dir / "dependencies").mkdir(exist_ok=True)
             if config.database != "None":
                 self._render_template(f"{template_base}/app/dependencies/db.py.jinja2", app_dir / "dependencies" / "db.py", config)
             (app_dir / "dependencies" / "__init__.py").touch()

             # JWT Auth for FastAPI
             if "JWT / Auth Template" in config.features:
                 self._render_template(f"{template_base}/app/core/security.py.jinja2", app_dir / "core" / "security.py", config)
                 (app_dir / "api" / "v1" / "routers").mkdir(parents=True, exist_ok=True)
                 self._render_template(f"{template_base}/app/api/v1/routers/auth.py.jinja2", app_dir / "api" / "v1" / "routers" / "auth.py", config)

             # Mail Service for FastAPI
             if "Mail Service" in config.features:
                 self._render_template(f"{template_base}/app/core/mail.py.jinja2", app_dir / "core" / "mail.py", config)



        # Shared Config & Extensions for Flask
        if config.framework == "Flask":
            # Extensions Folder
            (app_dir / "extensions").mkdir(exist_ok=True)
            self._render_template(f"{template_base}/app/extensions/__init__.py.jinja2", app_dir / "extensions" / "__init__.py", config)
            
            if config.database != "None":
                self._render_template(f"{template_base}/app/extensions/db.py.jinja2", app_dir / "extensions" / "db.py", config)
            
            if "Mail Service" in config.features:
                self._render_template(f"{template_base}/app/extensions/mail.py.jinja2", app_dir / "extensions" / "mail.py", config)
                
            if "JWT / Auth Template" in config.features:
                self._render_template(f"{template_base}/app/extensions/jwt.py.jinja2", app_dir / "extensions" / "jwt.py", config)

            if "Redis / Cache" in config.features:
                self._render_template(f"{template_base}/app/extensions/cache.py.jinja2", app_dir / "extensions" / "cache.py", config)

            # Config Folder
            config_dir = app_dir / "config"
            config_dir.mkdir(exist_ok=True)
            self._render_template(f"{template_base}/config/__init__.py.jinja2", config_dir / "__init__.py", config)
            self._render_template(f"{template_base}/config/base.py.jinja2", config_dir / "base.py", config)
            self._render_template(f"{template_base}/config/development.py.jinja2", config_dir / "development.py", config)
            self._render_template(f"{template_base}/config/testing.py.jinja2", config_dir / "testing.py", config)
            self._render_template(f"{template_base}/config/production.py.jinja2", config_dir / "production.py", config)


        # Generate .env
        self._render_template("shared/.env.jinja2", project_dir / ".env", config)

        # Generate Migrations if Alembic selected and SQL DB
        if "Alembic / DB Migrations" in config.features and config.database in ["PostgreSQL", "MySQL", "SQLite"]:
            (project_dir / "migrations").mkdir(exist_ok=True)
            # In a real scenario, we might init alembic here or just create the folder

        # Generate Docker if selected
        if "Docker" in config.features:
            self.generate_docker(config, project_dir)

        # Generate CI if selected
        if "GitHub Actions CI" in config.features:
            self.generate_ci(config, project_dir)
            
        # Generate Tasks if Celery selected
        if "Celery / RQ Background Tasks" in config.features:
            tasks_dir = project_dir / "tasks"
            tasks_dir.mkdir(exist_ok=True)
            self._render_template("shared/tasks/__init__.py.jinja2", tasks_dir / "__init__.py", config)
            self._render_template("shared/tasks/example_task.py.jinja2", tasks_dir / "example_task.py", config)

        # Logging Setup
        if "Logging Setup" in config.features:
            if config.framework == "Flask":
                self._render_template("shared/logging_config.py.jinja2", app_dir / "logging_config.py", config)
            else:
                self._render_template("shared/logging_config.py.jinja2", app_dir / "core" / "logging.py", config)


        
        # Create standard clean architecture folders
        (app_dir / "models").mkdir(exist_ok=True)
        (app_dir / "services").mkdir(exist_ok=True)
        (app_dir / "repositories").mkdir(exist_ok=True)
        (app_dir / "routes").mkdir(exist_ok=True)
        (app_dir / "utils").mkdir(exist_ok=True)
        
        if config.framework == "Flask":
            # Create routes/__init__.py for blueprint registration
            self._render_template(f"{template_base}/app/routes/__init__.py.jinja2", app_dir / "routes" / "__init__.py", config)
            self._render_template(f"{template_base}/app/repositories/base_repository.py.jinja2", app_dir / "repositories" / "base_repository.py", config)
            self._render_template(f"{template_base}/app/utils/email.py.jinja2", app_dir / "utils" / "email.py", config)
        else:
            self._render_template(f"{template_base}/app/utils/email.py.jinja2", app_dir / "utils" / "email.py", config)

        # Create __init__.py in subdirectories
        for subdir in ["models", "services", "repositories", "utils"]:
            (app_dir / subdir / "__init__.py").touch()
            
        # Save config
        config.save(project_dir / "archipyro.json")

    def _render_template(self, template_name: str, output_path: Path, config: ProjectConfig, **kwargs):
        if output_path.exists():
            should_overwrite = questionary.confirm(f"File {output_path} already exists. Overwrite?").ask()
            if not should_overwrite:
                print(f"Skipping {output_path}")
                return

        template = self.env.get_template(template_name)
        content = template.render(config=config, **kwargs)
        output_path.write_text(content)
        print(f"Created {output_path}")

    def generate_service(self, config: ProjectConfig, name: str, is_resource: bool = False):
        name_singular = self.p.singular_noun(name) or name
        template_path = f"{config.framework.lower()}/clean/service.py.jinja2"
        output_path = Path.cwd() / "app" / "services" / f"{name_singular.lower()}_service.py"
        self._render_template(template_path, output_path, config, name=name_singular, is_resource=is_resource)

    def generate_repository(self, config: ProjectConfig, name: str, is_resource: bool = False):
        name_singular = self.p.singular_noun(name) or name
        template_path = f"{config.framework.lower()}/clean/repository.py.jinja2"
        output_path = Path.cwd() / "app" / "repositories" / f"{name_singular.lower()}_repository.py"
        self._render_template(template_path, output_path, config, name=name_singular, is_resource=is_resource)

    def generate_model(self, config: ProjectConfig, name: str, is_resource: bool = False):
        name_singular = self.p.singular_noun(name) or name
        template_path = f"{config.framework.lower()}/clean/model.py.jinja2"
        output_path = Path.cwd() / "app" / "models" / f"{name_singular.lower()}.py"
        self._render_template(template_path, output_path, config, name=name_singular, is_resource=is_resource)

    def generate_route(self, config: ProjectConfig, name: str, is_resource: bool = False):
        name_singular = self.p.singular_noun(name) or name
        if config.framework == "Flask":
            template_path = "flask/clean/route.py.jinja2"
            output_path = Path.cwd() / "app" / "routes" / f"{name_singular.lower()}.py"
        else:
            template_path = "fastapi/clean/router.py.jinja2"
            output_path = Path.cwd() / "app" / "routes" / f"{name_singular.lower()}.py"
        self._render_template(template_path, output_path, config, name=name_singular, is_resource=is_resource)
        
        # Register the new route in the main app file
        self.register_route(config, name_singular)


    def generate_docker(self, config: ProjectConfig, project_dir: Path):
        self._render_template("shared/Dockerfile.jinja2", project_dir / "Dockerfile", config)
        self._render_template("shared/docker-compose.yml.jinja2", project_dir / "docker-compose.yml", config)

    def generate_ci(self, config: ProjectConfig, project_dir: Path):
        github_dir = project_dir / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        self._render_template("shared/ci.yml.jinja2", github_dir / "ci.yml", config)

    def generate_schema(self, config: ProjectConfig, name: str):
        name_singular = self.p.singular_noun(name) or name
        if config.framework == "FastAPI":
             template_path = "fastapi/clean/schema.py.jinja2"
             output_path = Path.cwd() / "app" / "schemas" / f"{name_singular.lower()}.py"
             (Path.cwd() / "app" / "schemas").mkdir(exist_ok=True)
             self._render_template(template_path, output_path, config, name=name_singular)


    def generate_resource(self, config: ProjectConfig, name: str):
        name_singular = self.p.singular_noun(name) or name
        self.generate_model(config, name_singular, is_resource=True)
        self.generate_repository(config, name_singular, is_resource=True)
        self.generate_service(config, name_singular, is_resource=True)
        self.generate_route(config, name_singular, is_resource=True)
        
        if config.framework == "FastAPI":
            self.generate_schema(config, name_singular)

    def register_route(self, config: ProjectConfig, name: str):
        """
        Register the new route in the main application file.
        """
        name_lower = name.lower()
        
        if config.framework == "Flask":
            # Flask: Add blueprint registration to app/routes/__init__.py
            routes_init = Path.cwd() / "app" / "routes" / "__init__.py"
            if not routes_init.exists():
                return
                
            content = routes_init.read_text()
            
            # Check if already registered
            if f"from app.routes.{name_lower} import {name_lower}_bp" in content:
                print(f"Blueprint {name_lower}_bp already registered")
                return
            
            # Add import and registration before the last line
            import_line = f"    from app.routes.{name_lower} import {name_lower}_bp\n"
            register_line = f"    app.register_blueprint({name_lower}_bp, url_prefix='/{name_lower}')\n"
            
            # Insert before the comment line "# Additional blueprints..."
            if "# Additional blueprints will be registered here automatically" in content:
                new_content = content.replace(
                    "    # Additional blueprints will be registered here automatically",
                    f"{import_line}{register_line}    # Additional blueprints will be registered here automatically"
                )
                routes_init.write_text(new_content)
                print(f"Registered blueprint {name_lower}_bp in app/routes/__init__.py")
            else:
                print(f"Warning: Could not find registration marker in app/routes/__init__.py")

        else:
            # FastAPI: Register router in app/main.py
            main_file = Path.cwd() / "app" / "main.py"
            if not main_file.exists():
                return
                
            content = main_file.read_text()
            
            # Check if already registered
            if f"from app.routes.{name_lower} import router as {name_lower}_router" in content:
                return
                
            # Append registration at the end of file
            import_stmt = f"\nfrom app.routes.{name_lower} import router as {name_lower}_router"
            reg_stmt = f"\napp.include_router({name_lower}_router, prefix='/api/v1/{name_lower}', tags=['{name_lower}'])"
            
            main_file.write_text(content + import_stmt + reg_stmt)
            print(f"Registered router {name_lower}_router in app/main.py")

