# Existing imports and test methods...
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageClasses.LoginPage import LoginPage
from PageClasses.DashboardPage import DashboardPage

# Existing test methods...

def test_TC_SCRUM_115_001_valid_login_session_established(driver):
    ...<existing test code>...

# --- New test for TC_SCRUM74_001 appended below ---
from auto_scripts.Pages.TC_SCRUM74_001_TestPage import TC_SCRUM74_001_TestPage

def test_TC_SCRUM74_001_valid_login_workflow(driver):
    ...<existing test code>...

# --- New test for TC_LOGIN_006 appended below ---
from auto_scripts.Pages.TC_LOGIN_006_TestPage import TC_LOGIN_006_TestPage

@pytest.mark.tc_login_006
def test_TC_LOGIN_006_valid_username_empty_password(driver):
    """
    Test Case TC_LOGIN_006:
    1. Navigate to the login page
    2. Enter valid username (testuser@example.com)
    3. Leave password field empty
    4. Click Login
    5. Verify error message 'Password is required' is displayed
    """
    login_url = "https://app.example.com/login"
    username = "testuser@example.com"

    # Instantiate the page class
    test_page = TC_LOGIN_006_TestPage(driver)

    # Run the test scenario
    results = test_page.run_tc_login_006(username, login_url)

    # Stepwise assertions
    assert results['step_1']['success'], f"Step 1 failed: {results['step_1'].get('error', '')}"
    assert results['step_2']['success'], f"Step 2 failed: {results['step_2'].get('error', '')}"
    assert results['step_3']['success'], f"Step 3 failed: {results['step_3'].get('error', '')}"
    assert results['step_4']['success'], f"Step 4 failed: {results['step_4'].get('error', '')}"
    assert results['step_4']['error_message'] == 'Password is required', (
        f"Expected error message 'Password is required', got '{results['step_4']['error_message']}'"
    )
    assert results['still_on_login_page'], "User should remain on login page after failed login attempt"
