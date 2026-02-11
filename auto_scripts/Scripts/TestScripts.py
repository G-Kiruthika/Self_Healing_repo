# Existing imports
import pytest
from auto_scripts.Pages.TC_LOGIN_006_TestPage import TC_LOGIN_006_TestPage

# ... (existing test methods) ...


def test_tc_login_006_remember_me_persistence():
    """
    TC_LOGIN_006: Validating 'Remember Me' session persistence on login.
    Steps:
    1. Navigate to login page
    2. Enter valid credentials
    3. Check 'Remember Me'
    4. Click Login
    5. Close and reopen browser, revisit site, and validate session persistence
    """
    # Instantiate the page class
    test_page = TC_LOGIN_006_TestPage()
    # Run the test case workflow
    result = test_page.run_tc_login_006('validuser@example.com', 'ValidPass123!')
    # Assert that the test case passed overall
    assert result['overall_pass'] is True, f"TC_LOGIN_006 failed: {result}"
