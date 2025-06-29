## StackExplain

Explain programming error messages using LLMs.

## Description 
StackExplain is a website, backend API, and CLI tool that analyzes error messages and explains what causes them using large language models. It suggests fixes and includes relevant links to documentation.

## Installation (Development)

Clone the repository:
```
git clone https://github.com/adityapatwardhan1/stackexplain.git
```

Build the virtual environment and install dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a .env file from the provided template:
```
cp .env.example .env
```

To run the backend server:
```
cd backend/src/stackexplain
uvicorn app.main:app --reload
```

To run the frontend site:
```
cd frontend
npm install
npm run dev
```

To build the CLI tool:
```
cd backend
pip install -e .
```

## Design Choices
1. Project Structure

    Monorepo-style root containing separate frontend/ and backend/ directories to cleanly separate concerns.

    Backend uses a src/ layout:

    backend/
      ├── src/
      │   └── stackexplain/
      │       ├── app/
      │       ├── cli.py
      │       └── __init__.py
      ├── pyproject.toml
      ├── .env
      └── venv/

        The src/stackexplain folder contains the Python package source.

        This structure avoids issues where local imports accidentally shadow installed packages.

        It also aligns with modern Python packaging best practices.

2. Packaging & Installation

    Use PEP 621 compliant pyproject.toml for dependency and build metadata, making the project installable via pip install -e . in editable mode.

    CLI entry point is defined via pyproject.toml under [project.scripts], e.g.:

    [project.scripts]
    explainerr = "stackexplain.cli:main"

    Bundling with PyInstaller was not prioritized, as deployment is handled via standard Python installation (pip install). 
    Relying on pip for installation and dependency management keeps the developer experience simple and compatible with most environments.

3. Environment Configuration

    Use .env file for sensitive keys like OPENROUTER_API_KEY.

    Load environment variables via python-dotenv with robust path handling so the app runs reliably regardless of the current working directory.

4. Dependency Management

    Pin exact versions in pyproject.toml dependencies for reproducible installs.

    Use a requirements.txt for environments where pip install from a requirements file is preferred.