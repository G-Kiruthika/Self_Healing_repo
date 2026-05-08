# Python UI & API Automation Framework

A comprehensive test automation framework for UI and API testing using Python, Selenium, and Pytest.

## Project Structure

```
auto_scripts/func/
│
├── config/                 # Configuration files
│   └── config.yaml        # Main configuration
│
├── core/                  # Core framework utilities
│   ├── driver_factory.py  # WebDriver factory
│   └── selenium_wrapper.py # Selenium wrapper utilities
│
├── tests/                 # Test cases
│   ├── conftest.py       # Pytest fixtures and configuration
│   └── ui/               # UI test cases
│       ├── test_shortcuts_enable_save_destination.py
│       └── test_shortcuts_remove_destination.py
│
├── utils/                 # Utility modules
│   ├── logger.py         # Logging utility
│   └── screenshot_helper.py # Screenshot utility
│
├── logs/                  # Test execution logs
├── reports/               # Test reports
├── screenshots/           # Test screenshots
│
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
└── README.md             # This file
```

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome/Firefox/Edge browser installed

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` to configure:

- Browser settings (chrome, firefox, edge, safari)
- Timeouts and waits
- Application URLs
- Test data paths
- Reporting options
- Logging levels

## Running Tests

### Run all tests

```bash
pytest
```

### Run specific test file

```bash
pytest tests/ui/test_shortcuts_enable_save_destination.py
```

### Run tests with markers

```bash
pytest -m ui          # Run only UI tests
pytest -m smoke       # Run only smoke tests
pytest -m regression  # Run only regression tests
```

### Run tests in parallel

```bash
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 parallel workers
```

### Run with HTML report

```bash
pytest --html=reports/report.html --self-contained-html
```

### Run in headless mode

Edit `config/config.yaml` and set `headless: true`

## Test Cases

### Test Case 82: Remove Save Destination Shortcut

**File:** `tests/ui/test_shortcuts_remove_destination.py`

**Description:** Verify the screen when user removes the 'Save' destination shortcut.

**Expected Result:** Remove this destination?' pop up should be displayed.

### Test Case 55: Enable Save Destination Toggle

**File:** `tests/ui/test_shortcuts_enable_save_destination.py`

**Description:** Verify the behavior when user Enables the 'Save' destination toggle bar in 'Add Shortcut' screen.

**Expected Result:** User should be able to Enable the 'Save' destination toggle bar. After disabling, 'continue' button should be enabled.

## Page Objects

Page objects are located in `auto_scripts/Pages/` directory:

- `root_view_screen.py` - Root view screen of the HPX app
- `printer_details_screen.py` - Printer details screen
- `shortcuts_screen.py` - Shortcuts management screen
- `add_shortcut_screen.py` - Add Shortcut configuration screen
- `remove_destination_popup.py` - Remove destination popup dialog

## Framework Features

### Core Utilities

- **Driver Factory:** Automatic WebDriver management with webdriver-manager
- **Selenium Wrapper:** Enhanced wait and interaction methods
- **Logger:** Comprehensive logging with file and console output
- **Screenshot Helper:** Automatic screenshot capture on failures

### Test Fixtures

- **driver:** WebDriver instance with automatic setup/teardown
- **config:** Configuration loaded from YAML
- **base_url:** Application base URL from config

### Reporting

- HTML reports with pytest-html
- Allure reports (optional)
- Screenshots on test failures
- Detailed logging

## Coding Standards

- **File naming:** lowercase_with_underscores
- **Class naming:** PascalCase
- **Method naming:** snake_case
- **Test naming:** test_feature_action

## Best Practices

1. Use Page Object Model (POM) for UI tests
2. Keep tests independent and isolated
3. Use descriptive test and method names
4. Add docstrings to classes and methods
5. Use pytest fixtures for setup/teardown
6. Implement proper waits (explicit over implicit)
7. Handle exceptions appropriately
8. Take screenshots on failures
9. Log important actions and verifications

## Troubleshooting

### WebDriver issues

- Ensure browser is installed
- Check browser version compatibility
- Update webdriver-manager: `pip install --upgrade webdriver-manager`

### Test failures

- Check logs in `logs/` directory
- Review screenshots in `screenshots/` directory
- Verify locators in page objects
- Check configuration in `config/config.yaml`

### Import errors

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python path configuration
- Verify project structure

## Contributing

1. Follow coding standards
2. Add tests for new features
3. Update documentation
4. Run tests before committing
5. Use meaningful commit messages

## Support

For issues and questions, please refer to the framework documentation or contact the automation team.
