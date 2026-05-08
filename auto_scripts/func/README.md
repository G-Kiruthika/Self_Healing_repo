# Python UI & API Automation Framework

A comprehensive test automation framework for UI and API testing using Python, Selenium, and Pytest.

## Project Structure

```
auto_scripts/func/
│
├── config/                 # Configuration files
│   └── config.yaml        # Environment and test configuration
│
├── core/                  # Core framework utilities
│   ├── driver_factory.py  # WebDriver factory
│   └── selenium_wrapper.py # Selenium utility methods
│
├── pages/                 # Page Object Model classes
│   ├── base_page.py       # Base page class
│   ├── hpx_app_launch_page.py
│   ├── printer_details_page.py
│   ├── shortcuts_page.py
│   └── remove_popup_page.py
│
├── tests/                 # Test cases
│   ├── conftest.py        # Pytest fixtures and configuration
│   └── ui/                # UI test cases
│       └── test_remove_print_shortcut.py
│
├── utils/                 # Utility modules
│   └── send_email_report.py
│
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
└── README.md             # This file
```

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **WebDriver Factory**: Flexible driver creation supporting Chrome, Firefox, and Edge
- **Configuration Management**: YAML-based configuration for environments and test data
- **Pytest Integration**: Powerful test framework with fixtures and markers
- **Reporting**: HTML reports and screenshot capture on test failures
- **Email Notifications**: Automated email reports for test results
- **Parallel Execution**: Support for parallel test execution

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` to configure:
- Browser settings (Chrome, Firefox, Edge)
- Timeouts and waits
- Application URLs
- Test data
- Email settings
- Logging preferences

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/ui/test_remove_print_shortcut.py
```

### Run specific test
```bash
pytest tests/ui/test_remove_print_shortcut.py::test_verify_remove_popup_displayed
```

### Run with markers
```bash
pytest -m smoke
pytest -m ui
```

### Run in parallel
```bash
pytest -n auto
```

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

## Writing Tests

### Test Structure

Tests follow the Arrange-Act-Assert pattern:

```python
def test_example():
    # Arrange: Set up test data and objects
    driver = get_driver()
    page = ExamplePage(driver)
    
    # Act: Perform actions
    page.perform_action()
    
    # Assert: Verify results
    assert page.verify_result()
    
    # Cleanup
    driver.quit()
```

### Using Fixtures

```python
def test_with_fixture(driver):
    page = ExamplePage(driver)
    page.perform_action()
    assert page.verify_result()
```

### Page Object Example

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ExamplePage(BasePage):
    BUTTON = (By.ID, 'example-button')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_button(self):
        self.click_element(self.BUTTON)
```

## Coding Standards

- **File Naming**: lowercase_with_underscores.py
- **Class Naming**: PascalCase
- **Method Naming**: snake_case
- **Test Naming**: test_feature_action
- **Docstrings**: All classes and methods should have docstrings

## Best Practices

1. **Use Page Object Model**: Keep test logic separate from page interactions
2. **Use Explicit Waits**: Avoid implicit waits and sleeps
3. **Keep Tests Independent**: Each test should be able to run independently
4. **Use Meaningful Names**: Test and method names should be descriptive
5. **Handle Exceptions**: Use try-finally blocks to ensure cleanup
6. **Use Fixtures**: Leverage pytest fixtures for setup and teardown
7. **Add Assertions**: Every test should have at least one assertion

## Troubleshooting

### WebDriver Issues
- Ensure webdriver-manager is installed
- Check browser version compatibility
- Verify network connectivity for driver downloads

### Test Failures
- Check screenshots in `screenshots/` directory
- Review logs in `logs/` directory
- Verify configuration in `config/config.yaml`

### Import Errors
- Ensure all dependencies are installed
- Check Python path configuration
- Verify project structure

## Contributing

1. Follow the coding standards
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass before committing

## Support

For issues and questions, please contact the QA Automation team.
