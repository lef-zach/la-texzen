# Contributing to LaTeXZen

Thank you for your interest in contributing to LaTeXZen! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Submitting Changes](#submitting-changes)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Encouraged Behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable Behavior:**
- Harassment or discriminatory language
- Trolling or insulting/derogatory comments
- Public or private harassment
- Publishing others' private information without consent
- Other conduct that could reasonably be considered inappropriate

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate corrective action in response to any instances of unacceptable behavior.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Docker (optional)
- LaTeX distribution (for PDF compilation)

### Setting Up Development Environment

```bash
# 1. Fork the repository
# Go to: https://github.com/lef-zach/la-texzen/fork

# 2. Clone your fork
git clone git@github.com:YOUR-USERNAME/la-texzen.git
cd la-texzen

# 3. Add upstream remote
git remote add upstream git@github.com:lef-zach/la-texzen.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
. venv/Scripts/activate   # Windows

# 5. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# 6. Install pre-commit hooks
pre-commit install
```

### Finding Issues to Work On

1. **Good First Issues**: Look for issues labeled `good-first-issue`
2. **Bug Fixes**: Issues labeled `bug`
3. **Features**: Issues labeled `enhancement`
4. **Documentation**: Issues labeled `documentation`

---

## Development Process

### Branch Naming Convention

```
# Feature branches
feature/short-description

# Bug fix branches
fix/issue-number-short-description

# Documentation branches
docs/short-description

# Example
feature/add-latex-preview
fix/123-login-error
docs/update-api-docs
```

### Workflow

```bash
# 1. Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes
# ... edit files ...

# 4. Test changes
pytest tests/

# 5. Commit changes
git add .
git commit -m "feat: Add new feature description"

# 6. Push to your fork
git push origin feature/your-feature

# 7. Create Pull Request
# Go to: https://github.com/lef-zach/la-texzen/compare
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Example:**
```
feat(templates): Add IEEE template validation

- Validate IEEE template structure
- Check required sections
- Return helpful error messages

Closes #123
```

---

## Submitting Changes

### Pull Request Process

1. **Update Documentation**: Ensure all new features are documented
2. **Update Tests**: Add tests for new functionality
3. **Check Formatting**: Run code formatters
4. **Run Tests**: Ensure all tests pass
5. **Describe Changes**: Provide clear PR description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature causing changes)
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review of code
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs
2. **Code Review**: Maintainers review code
3. **Feedback**: Address any comments
4. **Approval**: PR approved and merged
5. **Deploy**: Changes deployed to production

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Use Black for formatting
black app/ tests/

# Use isort for imports
isort app/ tests/

# Use flake8 for linting
flake8 app/ tests/
```

### Code Quality Tools

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Check code style
flake8 app/ tests/

# Type checking
mypy app/ tests/

# All checks
make quality
```

### Type Hints

```python
# Good
def process_document(file_path: str, format: str) -> dict:
    ...

# Bad
def process_document(file_path, format):
    ...
```

### Docstrings

```python
def create_team(name: str, description: str = "") -> Team:
    """Create a new team.
    
    Args:
        name: The name of the team
        description: Optional description of the team
        
    Returns:
        The created Team object
        
    Raises:
        ValueError: If team name is empty
    """
    if not name:
        raise ValueError("Team name cannot be empty")
    ...
```

### Comments

- Use comments for complex logic
- Avoid obvious comments
- Keep comments up-to-date
- Use clear, concise language

---

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Pytest configuration
├── unit/                 # Unit tests
│   ├── test_auth.py
│   ├── test_teams.py
│   └── ...
├── integration/          # Integration tests
│   └── test_api.py
└── fixtures/             # Test fixtures
    ├── test_user.py
    └── ...
```

### Writing Tests

```python
# tests/unit/test_teams.py
import pytest
from app.models import Team

def test_create_team():
    """Test team creation."""
    team = Team(name="Test Team", description="Test Description")
    
    assert team.name == "Test Team"
    assert team.description == "Test Description"

def test_team_str_representation():
    """Test team string representation."""
    team = Team(name="Test Team")
    
    assert str(team) == "Test Team"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_teams.py

# Run specific test
pytest tests/unit/test_teams.py::test_create_team

# Run with verbose output
pytest -v

# Run with marks
pytest -m "slow"
```

### Test Fixtures

```python
# tests/conftest.py
import pytest
from app.models import User, Team

@pytest.fixture
def test_user():
    return User(email="test@example.com", name="Test User")

@pytest.fixture
def test_team():
    return Team(name="Test Team", description="Test Description")
```

---

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings in code
2. **API Documentation**: Endpoint documentation
3. **User Documentation**: User guides
4. **Developer Documentation**: Architecture, setup guides

### Documentation Standards

- Use clear, concise language
- Include code examples
- Update documentation with code changes
- Use Markdown formatting
- Add diagrams where helpful

### Updating Documentation

```bash
# Documentation files are in docs/
# Update relevant files:
# - API.md
# - SETUP.md
# - ARCHITECTURE.md
# - DEPLOYMENT.md
```

---

## GitHub Actions

### Automated Checks

We use GitHub Actions for:

- **Code Quality**: Black, isort, flake8, mypy
- **Testing**: pytest with coverage
- **Security**: Vulnerability scanning
- **Docker**: Build and push Docker images

### Workflow Files

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=app
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Recognition

Contributors will be recognized in:

1. **CONTRIBUTORS.md**: List of all contributors
2. **Release Notes**: Mention of significant contributions
3. **Documentation**: Credit for documentation improvements

---

## Questions?

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and discussions
- **Email**: For security-related issues

---

Thank you for contributing to LaTeXZen! Your contributions help make this project better for everyone.
