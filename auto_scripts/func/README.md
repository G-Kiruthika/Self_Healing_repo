# Functional UI Automation Framework

## Overview
This is a Python-based functional UI automation framework for UnionDigital Bank, built using Selenium WebDriver and Pytest. The framework follows the Page Object Model (POM) design pattern and adheres to industry-standard coding practices.

## Project Structure
```
auto_scripts/func/
│
├── config/                     # Configuration files
│   └── config.yaml            # Environment and test configuration
│
├── core/                      # Core framework utilities
│   ├── driver_factory.py     # WebDriver factory
│   └── selenium_wrapper.py   # Selenium wrapper utilities
│
├── metadata/                  # Test metadata and documentation
│   └── test_metadata.json    # Test case metadata
│
├── tests/                     # Test cases
│   ├── conftest.py           # Pytest configuration and fixtures
│   └── ui/                   # UI test cases
│       └── test_loan_payment_guides.py
│
├── utils/                     # Utility modules
│   ├── logger.py             # Logging utilities
│   └── report_helper.py      # Reporting utilities
│
├── reports/                   # Test reports and screenshots
│   └── screenshots/          # Test failure screenshots
│
├── logs/                      # Log files
│
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Chrome/Firefox/Edge browser

### Installation
1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd auto_scripts/func
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit `config/config.yaml` to customize:
- Base URL
- Browser settings (chrome/firefox/edge)
- Timeouts
- Reporting options

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/ui/test_loan_payment_guides.py
```

### Run specific test:
```bash
pytest tests/ui/test_loan_payment_guides.py::TestLoanPaymentGuides::test_scrum_23804_ts_003_tc_001
```

### Run with specific browser:
```bash
pytest --browser=firefox
```

### Run in headless mode:
```bash
pytest --headless
```

### Generate HTML report:
```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Cases

### Test Case 352 - SCRUM-23804 TS-003 TC-001
**Description:** Verify '+' icon expands payment options on UD Loans Payment Guide page

**Steps:**
1. Launch browser
2. Navigate to homepage
3. Click 'Loan Payment Guides' link
4. Click 'UD Loans' link
5. Locate 'How To Pay' section
6. Click expand payment options icon
7. Verify payment option details are displayed

### Test Case 353 - SCRUM-23804 TS-004 TC-001
**Description:** Verify UPAY payment link is visible after expanding payment options

**Steps:**
1. Launch browser
2. Navigate to homepage
3. Click 'Loan Payment Guides' link
4. Click 'UD Loans' link
5. Click expand payment options icon
6. Locate UPAY section
7. Verify 'Click here to pay via UPAY' link is visible

## Framework Features
- **Page Object Model (POM):** Separation of page elements and test logic
- **Driver Factory:** Centralized WebDriver management
- **Configuration Management:** YAML-based configuration
- **Reporting:** HTML reports with screenshots on failure
- **Logging:** Comprehensive logging for debugging
- **Pytest Integration:** Powerful test execution and fixtures
- **Cross-browser Support:** Chrome, Firefox, Edge

## Coding Standards
- **File Naming:** lowercase_with_underscores
- **Class Naming:** PascalCase
- **Method Naming:** snake_case
- **Test Naming:** test_feature_action

## Page Objects
Page objects are located in `auto_scripts/Pages/`:
- `home_page.py` - HomePage class
- `loan_payment_guides_page.py` - LoanPaymentGuidesPage class
- `ud_loans_payment_guide_page.py` - UdLoansPaymentGuidePage class

## Reporting
- HTML reports are generated in `reports/`
- Screenshots of failures are saved in `reports/screenshots/`
- Logs are saved in `logs/`

## Troubleshooting
- Ensure WebDriver is compatible with your browser version
- Check `config.yaml` for correct URL and settings
- Review logs in `logs/automation.log` for detailed error information
- Screenshots of failures are available in `reports/screenshots/`

## Contributing
Follow the coding standards and framework architecture when adding new tests or features.

## Contact
For questions or issues, please contact the QA Automation team.
