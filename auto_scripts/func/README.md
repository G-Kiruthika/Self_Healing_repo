# Functional UI Automation Framework

## Overview
This is a Python-based UI automation framework for testing the HPX application, specifically focusing on Shortcuts functionality. The framework follows the Page Object Model (POM) design pattern and uses Selenium WebDriver for browser automation.

## Project Structure
```
auto_scripts/func/
├── config/
│   └── config.yaml              # Configuration settings
├── core/
│   ├── __init__.py
│   ├── driver_factory.py        # WebDriver factory
│   └── selenium_wrapper.py      # Selenium wrapper utilities
├── pages/
│   ├── __init__.py
│   ├── base_page.py             # Base page class
│   ├── hpx_app.py               # HPX App page object
│   ├── printer_details_screen.py # Printer Details page object
│   └── shortcuts_screen.py      # Shortcuts page object
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   └── ui/
│       ├── __init__.py
│       ├── test_remove_email_shortcut.py
│       └── test_cancel_email_shortcut_removal.py
├── utils/
│   ├── __init__.py
│   ├── logger.py                # Logging utility
│   └── screenshot_helper.py     # Screenshot utility
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
└── README.md                    # This file
```

## Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Chrome/Firefox/Edge browser installed

### Installation
1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd auto_scripts/func/
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit `config/config.yaml` to customize:
- Browser type (chrome, firefox, edge)
- Headless mode
- Timeouts
- Application URL
- Logging settings
- Screenshot settings

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/ui/test_remove_email_shortcut.py
```

### Run tests with markers
```bash
pytest -m shortcuts
pytest -m ui
```

### Run tests in parallel
```bash
pytest -n auto
```

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Cases

### Test Case 80: Verify Remove Email Shortcut
- **File**: `test_remove_email_shortcut.py`
- **Purpose**: Verify that email shortcut can be removed successfully
- **Flow**:
  1. Install and launch HPX app
  2. Navigate to printer details screen
  3. Click edit link on shortcuts screen
  4. Click email shortcut edit icon
  5. Click remove button
  6. Verify email destination is removed

### Test Case 81: Verify Cancel Email Shortcut Removal
- **File**: `test_cancel_email_shortcut_removal.py`
- **Purpose**: Verify that email shortcut removal can be canceled
- **Flow**:
  1. Install and launch HPX app
  2. Navigate to printer details screen
  3. Click edit link on shortcuts screen
  4. Click email shortcut edit icon
  5. Click cancel button
  6. Verify shortcuts screen is displayed correctly

## Framework Features

### Page Object Model (POM)
- All page interactions are encapsulated in page classes
- Reusable page methods
- Clear separation of test logic and page logic

### Driver Factory
- Centralized WebDriver creation
- Support for multiple browsers
- Configurable browser options
- Automatic driver management via webdriver-manager

### Base Page Class
- Common page operations (click, enter text, wait, etc.)
- Reusable across all page objects
- Consistent error handling

### Logging
- Automatic logging to file and console
- Configurable log levels
- Timestamped log entries

### Screenshots
- Automatic screenshots on test failure
- Manual screenshot capture
- Organized screenshot storage

### Configuration Management
- YAML-based configuration
- Environment-specific settings
- Easy configuration updates

## Best Practices

1. **Test Independence**: Each test should be independent and not rely on other tests
2. **Page Objects**: Use page objects for all UI interactions
3. **Explicit Waits**: Use explicit waits instead of implicit waits or sleep
4. **Assertions**: Use clear, descriptive assertion messages
5. **Cleanup**: Always cleanup resources (driver.quit()) in finally blocks or fixtures
6. **Naming**: Follow naming conventions (snake_case for functions, PascalCase for classes)

## Troubleshooting

### WebDriver Issues
- Ensure browser is installed and up to date
- Check webdriver-manager is properly installed
- Verify internet connection for driver download

### Test Failures
- Check screenshots in `screenshots/` directory
- Review logs in `logs/test_execution.log`
- Verify configuration in `config/config.yaml`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python path includes project root

## Contributing
1. Follow existing code structure and naming conventions
2. Add docstrings to all classes and methods
3. Write tests for new features
4. Update README for significant changes

## Support
For issues or questions, please contact the QA Automation team.
