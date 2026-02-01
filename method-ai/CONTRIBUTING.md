# Contributing to Method.AI

Thank you for your interest in contributing to Method.AI. This document provides guidelines and information for contributors.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Safety First

Given the nature of this project (generating chemical procedures), we have strict requirements:

1. **No Specific Hazardous Instructions**: Do not add code that generates specific instructions for hazardous reactions, weaponizable chemistry, or controlled substance synthesis.

2. **Maintain Disclaimers**: All generated output must include appropriate safety disclaimers. Do not remove or weaken existing safety warnings.

3. **Placeholder Over Specifics**: When in doubt, use generic placeholders rather than specific reagent names or detailed procedures.

4. **Review Carefully**: All PRs touching procedure generation logic require extra scrutiny.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend development)
- Git

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/method-ai.git
cd method-ai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install

# Copy environment file
cp .env.example .env
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

### Code Style

We use:
- **ruff** for linting and formatting Python code
- **mypy** for type checking

```bash
# Check code style
make lint

# Auto-format code
make format

# Type check
make type-check
```

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. Check existing issues and roadmap
2. Use the feature request template
3. Explain the use case and benefits
4. Consider safety implications

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add/update tests as needed
5. Ensure all tests pass (`make test`)
6. Ensure code is formatted (`make format`)
7. Commit with clear messages
8. Push to your fork
9. Open a pull request

### Commit Messages

Use clear, descriptive commit messages:

```
type: short description

Longer description if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Formatting changes
- `chore`: Maintenance tasks

## Project Structure

```
method-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── core/         # Configuration
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   └── tests/            # Tests
├── frontend/             # Next.js frontend
├── docs/                 # Documentation
└── examples/             # Example data
```

## Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage
- Tests must not require external API keys
- Use mocking for external services
- Include both happy path and error cases

## Documentation

- Update relevant documentation for changes
- Add docstrings to public functions
- Update API documentation if endpoints change
- Keep examples up to date

## Questions?

- Open a discussion on GitHub
- Check existing documentation
- Review closed issues

Thank you for contributing to Method.AI!
