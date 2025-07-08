# Tests for Dividends Analysis Application

This directory contains unit tests for the dividends analysis application.

## Test Structure

- `test_api_requests.py` - Tests for API request functions
- `test_app.py` - Tests for the main Dash application
- `test_utils.py` - Tests for utility functions

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
# Using pytest directly
python -m pytest tests/ -v

# Using the test runner script
python run_tests.py
```

### Run Specific Test File

```bash
# Run only API tests
python -m pytest tests/test_api_requests.py -v

# Run only app tests
python -m pytest tests/test_app.py -v

# Using the test runner script
python run_tests.py test_api_requests.py
```

### Run Tests with Coverage

```bash
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing -v
```

This will generate a coverage report in `htmlcov/index.html`

## Test Categories

### API Tests (`test_api_requests.py`)

- **Historical Dividends Tests**: Test functions that fetch historical dividend data
- **Investing.com API Tests**: Test the Investing.com API integration with error handling

### Application Tests (`test_app.py`)

- **App Initialization Tests**: Test that the app initializes correctly
- **Callback Tests**: Test Dash callbacks with various data scenarios
- **Error Handling Tests**: Test how the app handles errors and edge cases

### Utility Tests (`test_utils.py`)

- **Data Validation Tests**: Test data validation functions
- **Dividend Summary Tests**: Test dividend summary calculations

## Writing New Tests

When adding new functionality, please add corresponding tests:

1. Create a new test file or add to existing one
2. Follow the naming convention: `test_*.py` for files, `test_*` for functions
3. Use descriptive test names that explain what is being tested
4. Include both positive and negative test cases
5. Mock external dependencies (APIs, databases, etc.)

### Example Test Structure

```python
import pytest
from unittest.mock import patch, MagicMock

class TestNewFeature:
    """Test cases for new feature"""
    
    def test_feature_with_valid_input(self):
        """Test feature with valid input data"""
        # Arrange
        input_data = "valid_data"
        
        # Act
        result = some_function(input_data)
        
        # Assert
        assert result is not None
        assert result == expected_value
    
    def test_feature_with_invalid_input(self):
        """Test feature with invalid input data"""
        # Arrange
        input_data = None
        
        # Act & Assert
        with pytest.raises(ValueError):
            some_function(input_data)
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines to ensure code quality:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pip install -r requirements.txt
    python -m pytest tests/ --cov=. --cov-report=xml
```

## Coverage Goals

- Aim for at least 80% code coverage
- Focus on critical paths and error handling
- Test edge cases and error conditions 