# Contributing to Dremio CLI

Thank you for your interest in contributing to Dremio CLI!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-org/dremio-cli
cd dremio-cli
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dremio_cli --cov-report=html

# Run specific test file
pytest tests/test_config.py
```

## Code Quality

We use several tools to maintain code quality:

```bash
# Format code with black
black dremio_cli tests

# Sort imports with isort
isort dremio_cli tests

# Type checking with mypy
mypy dremio_cli

# Linting with flake8
flake8 dremio_cli tests
```

## Project Structure

```
dremio-cli/
├── dremio_cli/          # Main package
│   ├── client/          # API clients
│   ├── commands/        # CLI commands
│   ├── formatters/      # Output formatters
│   └── utils/           # Utilities
├── tests/               # Test suite
├── docs/                # Documentation
└── setup.py             # Package configuration
```

## Adding New Commands

1. Create a new file in `dremio_cli/commands/`
2. Define your command group using Click
3. Register it in `dremio_cli/cli.py`
4. Add tests in `tests/test_commands/`
5. Document in `docs/commands/`

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation
7. Submit a pull request

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions focused and small
- Add comments for complex logic

## Questions?

Open an issue or start a discussion on GitHub!
