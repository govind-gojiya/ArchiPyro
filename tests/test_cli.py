import os
from pathlib import Path
from archipyro.__main__ import app
from unittest.mock import patch

def test_init_command(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        with patch("archipyro.utils.prompt.ask_project_name", return_value="test_project"), \
             patch("archipyro.utils.prompt.ask_framework", return_value="Flask"), \
             patch("archipyro.utils.prompt.ask_architecture", return_value="Clean Architecture (Services + Repositories + Domain)"), \
             patch("archipyro.utils.prompt.ask_optional_features", return_value=[]):
            
            result = runner.invoke(app, ["init"])
            print(result.stdout)
            print(result.exception)
            assert result.exit_code == 0
            assert "Generating project: test_project" in result.stdout
            
            project_dir = Path("test_project")
            assert project_dir.exists()
            assert (project_dir / "archipyro.json").exists()
            assert (project_dir / "app" / "main.py").exists()

def test_add_service(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Init project first
        with patch("archipyro.utils.prompt.ask_project_name", return_value="test_project"), \
             patch("archipyro.utils.prompt.ask_framework", return_value="Flask"), \
             patch("archipyro.utils.prompt.ask_architecture", return_value="Clean Architecture (Services + Repositories + Domain)"), \
             patch("archipyro.utils.prompt.ask_optional_features", return_value=[]):
            runner.invoke(app, ["init"])
        
        os.chdir("test_project")
        result = runner.invoke(app, ["add", "service", "User"])
        assert result.exit_code == 0
        assert "Added service: User" in result.stdout
        
        assert Path("app/services/user_service.py").exists()

def test_gen_docker(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Init project first
        with patch("archipyro.utils.prompt.ask_project_name", return_value="test_project"), \
             patch("archipyro.utils.prompt.ask_framework", return_value="Flask"), \
             patch("archipyro.utils.prompt.ask_architecture", return_value="Clean Architecture (Services + Repositories + Domain)"), \
             patch("archipyro.utils.prompt.ask_optional_features", return_value=[]):
            runner.invoke(app, ["init"])
        
        os.chdir("test_project")
        result = runner.invoke(app, ["gen", "docker"])
        assert result.exit_code == 0
        assert "Generated Docker configuration" in result.stdout
        
        assert Path("Dockerfile").exists()
        assert Path("docker-compose.yml").exists()
