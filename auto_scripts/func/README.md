# Python UI & API Automation Framework

A comprehensive automation framework for UI and API testing using Python, Selenium, and Pytest.

## Project Structure

```
auto_scripts/func/
│
├── config/              # Configuration files
│   └── config.yaml     # Environment and test configuration
│
├── core/               # Core framework utilities
│   ├── __init__.py
│   ├── driver_factory.py    # WebDriver factory
│   └── selenium_wrapper.py  # Selenium wrapper utilities
│
├── pages/              # Page Object Models
│   ├── __init__.py
│   ├── base_page.py
│   ├── root_view_screen.py
│   ├── device_details_page.py
│   ├── shortcuts_screen.py
│   ├── create_shortcut_screen.py
│   ├── add_save_screen.py
│   └── delete_shortcut_popup.py
│
├── tests/              # Test cases
│   ├── __init__.py
│   ├── conftest.py     # Pytest fixtures and configuration
│   └── ui/             # UI test cases
│       ├── __init__.py
│       ├── test_shortcuts_cloud_signin.py
│       └── test_shortcuts_delete_popup.py
│
├── utils/              # Utility modules
│   └── __init__.py
│
├── requirements.txt    # Python dependencies
├── pytest.ini         # Pytest configuration
└── README.md          # This file
```

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Selenium Wrapper**: Robust element interaction methods with error handling
- **Driver Factory**: Support for multiple browsers (Chrome, Firefox, Edge)
- **Configuration Management**: YAML-based configuration for different environments
- **Pytest Integration**: Powerful test execution with fixtures and markers
- **Logging**: Comprehensive logging for debugging and reporting
- **HTML Reports**: Built-in HTML test reports

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Update `config/config.yaml` with your environment-specific settings:

- Browser type and settings
- Application URLs
- Timeouts and wait times
- Test data

## Running Tests

### Run all tests
```bash
pytest
```

### Run UI tests only
```bash
pytest tests/ui/
```

### Run specific test file
```bash
pytest tests/ui/test_shortcuts_cloud_signin.py`
```

### Run with markers
```bash
pytest -m ui
pytest -m smoke
```

### Run in headless mode
Update `config.yaml` to set `headless: true` or use environment variable

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Cases

### Test Case 72: Cloud Account Sign-In
- **File**: `tests/ui/test_shortcuts_cloud_signin.py`
- **Description**: Verify cloud account sign-in from Add Save screen
- **Flow**: Launch app → Navigate to shortcuts → Create shortcut → Sign in to cloud

### Test Case 73: Delete Shortcut Popup
- **File**: `tests/ui/test_shortcuts_delete_popup.py`
- **Description**: Verify button positions on delete shortcut popup
- **Flow**: Launch app → Navigate to shortcuts → Click delete → Verify buttons

## Writing New Tests

1. Create page object class in `pages/` inheriting from `BasePage`
2. Define locators and methods for page interactions
3. Create test file in `tests/ui/` or `tests/api/`
4. Use fixtures from `conftest.py` for driver and configuration
5. Follow naming conventions: `test_<feature>_<action>`

## Best Practices

- Use Page Object Model for all UI interactions
- Keep test methods focused and independent
- Use descriptive names for tests and methods
- Add docstrings to classes and methods
- Use pytest fixtures for setup and teardown
- Leverage markers for test categorization
- Handle exceptions appropriately
- Use explicit waits instead of sleep

## Troubleshooting

### WebDriver Issues
- Ensure webdriver-manager is installed
- Check browser version compatibility
- Update webdriver-manager: `pip install --upgrade webdriver-manager`

### Element Not Found
- Verify locators are correct
- Increase timeout in config.yaml
- Check if element is in iframe
- Ensure page is fully loaded

### Test Failures
- Check logs in `logs/` directory
- Review HTML report for details
- Enable screenshots on failure
- Run in non-headless mode for debugging

## Contributing

1. Follow the existing code structure and conventions
2. Add tests for new features
3. Update documentation as needed
4. Ensure all tests pass before committing

## License

Internal use only.
