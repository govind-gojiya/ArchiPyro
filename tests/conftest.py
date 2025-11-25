import pytest
from typer.testing import CliRunner
from archipyro.__main__ import app

@pytest.fixture
def runner():
    return CliRunner()
