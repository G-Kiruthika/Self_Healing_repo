# Functional UI Automation Framework

## Overview
This is a Python-based UI automation framework using Selenium WebDriver and Pytest for functional testing.

## Project Structure
```
auto_scripts/func/
├── config/
│   └── config.yaml          # Configuration file for environments and settings
├── core/
│   ├── driver_factory.py    # WebDriver initialization and management
│   └── selenium_wrapper.py  # Selenium utility wrapper (if needed)
├── pages/
│   ├── base_page.py         # Base page class with common methods
│   ├── root_view_screen.py  # Root view page object
│   ├── device_details_page.py
│   ├── shortcuts_screen.py
│   ├── create_shortcut_screen.py
│   ├── add_save_screen.py
│   └── delete_shortcut_popup.py
├── tests/
│   ├── conftest.py          # Pytest fixtures and configuration
│   └── ui/
│       ├── test_shortcuts_sign_in.py
│       └── test_delete_shortcut_popup.py
├── reports/                 # Test reports and screenshots
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Chrome/Firefox/Edge browser installed

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd auto_scripts/func
```

2. Create virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure settings
- Update `config/config.yaml` with your application URL and preferences
- Set browser type, timeouts, and other configurations

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/ui/test_shortcuts_sign_in.py
```

### Run specific test case
```bash
pytest tests/ui/test_shortcuts_sign_in.py::TestShortcutsSignIn::test_sign_in_link_cloud_accounts
```

### Run tests with markers
```bash
# Run only UI tests
pytest -m ui

# Run smoke tests
pytest -m smoke

# Run shortcuts tests
pytest -m shortcuts
```

### Run tests in parallel
```bash
pytest -n auto
```

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

## Configuration

### Browser Configuration
Edit `config/config.yaml` to change browser settings:
```yaml
ui:
  browser: "chrome"  # Options: chrome, firefox, edge
  headless: false    # Set to true for headless execution
  implicit_wait: 10
  explicit_wait: 20
```

### Test Data
Test data can be configured in `config/config.yaml` under the `test_data` section.

## Page Object Model (POM)

This framework follows the Page Object Model design pattern:

- **Base Page**: `pages/base_page.py` - Contains common methods used across all pages
- **Page Classes**: Each page/screen has its own class with locators and methods
- **Test Files**: Tests use page objects to interact with the application

### Example Page Object
```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ExamplePage(BasePage):
    # Locators
    BUTTON = (By.ID, "button-id")
    
    # Methods
    def click_button(self):
        self.click_element(self.BUTTON)
    
    def is_button_visible(self):
        return self.is_element_visible(self.BUTTON)
```

## Writing Tests

### Test Structure
```python
import pytest
from pages.example_page import ExamplePage

class TestExample:
    def test_example_functionality(self, driver):
        """Test description."""
        page = ExamplePage(driver)
        page.click_button()
        assert page.is_button_visible()
```

### Using Fixtures
The `driver` fixture is automatically available in all tests via `conftest.py`.

## Best Practices

1. **Use Page Objects**: Always interact with UI through page objects
2. **Explicit Waits**: Use explicit waits for dynamic elements
3. **Descriptive Names**: Use clear, descriptive names for tests and methods
4. **Independent Tests**: Each test should be independent and able to run in any order
5. **Assertions**: Include clear assertions with meaningful messages
6. **Documentation**: Add docstrings to test methods explaining what they test

## Troubleshooting

### WebDriver Issues
- Ensure browser is installed and up to date
- `webdriver-manager` automatically downloads the correct driver version
- Check browser compatibility with Selenium version

### Test Failures
- Check screenshots in `reports/screenshots/` (if enabled)
- Review logs in `reports/pytest.log`
- Verify element locators are correct
- Check timeouts in configuration

## Contributing

1. Follow the existing code structure and naming conventions
2. Add appropriate tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass before committing

## Support

For issues or questions, please contact the QA automation team.
