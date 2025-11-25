import sys
import os
from pathlib import Path
from archipyro.core.config import ProjectConfig
from archipyro.core.generator import Generator
import pytest

def test_generated_flask_project_runs(tmp_path):
    import sys
    print(f"Python executable: {sys.executable}")
    print(f"Sys path: {sys.path}")
    try:
        import flask
        print(f"Flask version: {flask.__version__}")
    except ImportError as e:
        print(f"Could not import flask: {e}")

    # Generate Flask project
    config = ProjectConfig(
        name="flask_run_test",
        framework="Flask",
        architecture="Clean Architecture",
        features=[]
    )
    generator = Generator()
    
    # We need to generate in tmp_path, but Generator uses cwd.
    # So we change cwd to tmp_path
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        generator.generate_project(config)
        
        project_dir = tmp_path / "flask_run_test"
        sys.path.insert(0, str(project_dir))
        
        from app import create_app
        app = create_app()
        assert app is not None
        
    finally:
        os.chdir(cwd)
        if str(project_dir) in sys.path:
            sys.path.remove(str(project_dir))
        if "app" in sys.modules:
            del sys.modules["app"]
        if "app.routes" in sys.modules:
            del sys.modules["app.routes"]
        if "app.main" in sys.modules:
            del sys.modules["app.main"]

def test_generated_fastapi_project_runs(tmp_path):
    # Generate FastAPI project
    config = ProjectConfig(
        name="fastapi_run_test",
        framework="FastAPI",
        architecture="Clean Architecture",
        features=[]
    )
    generator = Generator()
    
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        generator.generate_project(config)
        
        project_dir = tmp_path / "fastapi_run_test"
        sys.path.insert(0, str(project_dir))
        
        from app.main import app
        assert app is not None
        
    finally:
        os.chdir(cwd)
        if str(project_dir) in sys.path:
            sys.path.remove(str(project_dir))
        if "app" in sys.modules:
            del sys.modules["app"]
        if "app.main" in sys.modules:
            del sys.modules["app.main"]
