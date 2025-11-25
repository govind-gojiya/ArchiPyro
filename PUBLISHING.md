# Publishing ArchiPyro to PyPI

This guide explains how to build and publish the **ArchiPyro** package to the Python Package Index (PyPI).

## Prerequisites

Ensure you have the necessary tools installed:

```bash
pip install build twine
```

You will also need a PyPI account. Register at [pypi.org](https://pypi.org/).

## 1. Update Version

Before publishing, make sure to update the version number in `pyproject.toml` (or `setup.py` if you are using it).

```toml
# pyproject.toml
[project]
version = "0.1.0"  # Update this!
```

## 2. Build the Package

Run the following command to generate the distribution archives (source archive and wheel):

```bash
python -m build
```

This will create a `dist/` directory containing:
- `archipyro-0.1.0.tar.gz` (Source Archive)
- `archipyro-0.1.0-py3-none-any.whl` (Wheel)

## 3. Check the Package

It's good practice to check your distribution files for any errors before uploading:

```bash
twine check dist/*
```

## 4. Test Publish (Optional but Recommended)

You can upload to TestPyPI first to verify everything works without affecting the real PyPI.

1. Register at [test.pypi.org](https://test.pypi.org/).
2. Upload:

```bash
twine upload --repository testpypi dist/*
```

3. Try installing it:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ archipyro
```

## 5. Publish to PyPI

Once you are ready, upload the package to the real PyPI:

```bash
twine upload dist/*
```

You will be prompted for your username (`__token__`) and password (your API token).

## 6. Verification

Visit your project page on PyPI: [https://pypi.org/project/archipyro/](https://pypi.org/project/archipyro/)

You can now install your package globally:

```bash
pip install archipyro
```

## Automation (GitHub Actions)

You can automate this process using GitHub Actions. Create a workflow file `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Remember to add `PYPI_API_TOKEN` to your GitHub repository secrets.
