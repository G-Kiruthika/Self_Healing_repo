# Functional Automation Test Suite

## Overview
This directory contains functional automation tests for the HPX mobile application, specifically focusing on shortcut management and email destination features.

## Project Structure
```
auto_scripts/func/
├── config/
│   └── config.yaml          # Test configuration
├── tests/
│   ├── conftest.py          # Pytest fixtures and configuration
│   └── ui/
│       └── test_add_shortcut_email_destination.py  # Test cases
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Test Suite: AddShortcutEmailDestination

### Test Case ID: 63
**Description:** Verify the screen when the user enables only the 'Email' destination in the 'Add Shortcut' screen.

**Test Flow:**
1. Install and Launch the HPX app
2. Click on the printer icon on the root view screen
3. Click on the shortcuts tile on the device details page
4. Click on Add new shortcuts in shortcuts screen
5. Click on the Create your own shortcut arrow button
6. Enable only the 'Email' destination toggle bar in 'Add Shortcut' screen
7. Click on the Continue button
8. Verify the screen

**Expected Result:** User should be navigated to the 'Add Email' screen.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Appium Server 2.0+
- Android SDK (for Android testing)
- Mobile device or emulator

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Appium capabilities:
   - Edit `config/config.yaml`
   - Update the `app` path to your HPX APK location
   - Adjust device settings as needed

3. Start Appium server:
```bash
appium
```

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run specific test file:
```bash
pytest tests/ui/test_add_shortcut_email_destination.py
```

### Run with verbose output:
```bash
pytest -v tests/
```

### Run with HTML report:
```bash
pytest --html=report.html tests/
```

### Run specific test case:
```bash
pytest tests/ui/test_add_shortcut_email_destination.py::test_verify_email_destination_screen
```

## Configuration

### Appium Configuration
Edit `config/config.yaml` to modify:
- Platform settings (Android/iOS)
- Device capabilities
- App package and activity
- Timeouts and wait settings

### Test Settings
- `screenshot_on_failure`: Capture screenshots on test failures
- `retry_count`: Number of retry attempts for flaky tests
- `timeout`: Default timeout for element waits

## Page Objects

This test suite uses the following Page Objects:
- `RootViewScreen`: Main application screen
- `DeviceDetailsPage`: Device details and settings
- `ShortcutsScreen`: Shortcuts management screen
- `CreateShortcutScreen`: Create new shortcut screen
- `AddShortcutScreen`: Add shortcut configuration screen

All Page Objects are located in `auto_scripts/Pages/` directory.

## Reporting

Test results can be generated in multiple formats:
- Console output (default)
- HTML report (`--html=report.html`)
- Allure report (if allure-pytest is configured)

## Troubleshooting

### Common Issues

1. **Appium connection failed:**
   - Ensure Appium server is running
   - Check `appium_server_url` in config.yaml

2. **Element not found:**
   - Verify accessibility IDs in Page Objects
   - Increase implicit wait timeout in config

3. **App installation failed:**
   - Check app path in config.yaml
   - Ensure device/emulator is connected

## Best Practices

1. Always use Page Object Model pattern
2. Follow naming conventions (snake_case for functions/files)
3. Add descriptive docstrings to test functions
4. Use fixtures for setup and teardown
5. Keep test data in configuration files

## Contributing

When adding new tests:
1. Follow the existing project structure
2. Use appropriate Page Objects
3. Add test documentation
4. Update this README if needed

## Contact

For questions or issues, please contact the QA Automation team.
