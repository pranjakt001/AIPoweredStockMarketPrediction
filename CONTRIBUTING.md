# Contributing to AI Stock Market Prediction

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professionalism

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Logs/screenshots if applicable

### Suggesting Features

1. Check existing feature requests
2. Use the feature request template
3. Explain:
   - The problem it solves
   - Proposed solution
   - Alternative solutions considered
   - Additional context

### Pull Requests

#### Before Starting

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Discuss major changes in an issue first

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AIPoweredStockMarketPrediction.git
cd AIPoweredStockMarketPrediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8
```

#### Making Changes

1. **Code Style**
   - Follow PEP 8
   - Use Black for formatting: `black backend/`
   - Run linter: `flake8 backend/`

2. **Write Tests**
   - Add tests for new features
   - Ensure existing tests pass
   - Run tests: `pytest tests/`

3. **Documentation**
   - Update README if needed
   - Add docstrings to functions
   - Update API docs for endpoint changes

4. **Commits**
   - Use clear commit messages
   - Follow conventional commits format:
     - `feat: Add new feature`
     - `fix: Fix bug in prediction`
     - `docs: Update README`
     - `test: Add tests for API`
     - `refactor: Improve code structure`

#### Submitting PR

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push changes**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create PR**
   - Clear title and description
   - Reference related issues
   - Include screenshots for UI changes
   - Check all CI tests pass

4. **PR Checklist**
   - [ ] Code follows style guidelines
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   - [ ] All tests pass
   - [ ] No merge conflicts

## Development Guidelines

### Python Code

```python
def function_name(param1: str, param2: int) -> dict:
    """
    Brief description.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
    """
    pass
```

### API Endpoints

- Use RESTful conventions
- Proper HTTP methods (GET, POST, PUT, DELETE)
- Return appropriate status codes
- Include error handling
- Add logging

### Frontend

- Vanilla JavaScript (no frameworks currently)
- Responsive design
- Accessibility (ARIA labels)
- Cross-browser compatibility

## Testing

### Unit Tests

```python
def test_function_name():
    """Test description"""
    # Arrange
    input_data = {...}

    # Act
    result = function_name(input_data)

    # Assert
    assert result == expected_output
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_api.py

# With coverage
pytest --cov=backend tests/
```

## Project Structure

```
backend/
├── api/          # API routes
├── models/       # ML models
├── services/     # Business logic
├── utils/        # Utilities
└── config/       # Configuration

frontend/
├── index.html    # Main page
├── styles/       # CSS
└── src/          # JavaScript

tests/            # Test suite
docs/             # Documentation
scripts/          # Utility scripts
```

## Questions?

- Open an issue for questions
- Join discussions
- Check documentation first

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Appreciated in README

Thank you for contributing! 🎉
