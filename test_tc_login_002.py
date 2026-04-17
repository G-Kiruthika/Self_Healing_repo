"""
Test Script for TC_LOGIN_008: Negative Login (Unregistered Email)
This test automates the scenario where an unregistered email and any password are entered, and verifies error handling and page state.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_002_negative_unregistered_email(driver):
    """
    Test Case TC_LOGIN_008: Negative Login Workflow (Unregistered Email)
    Steps:
        1. Navigate to login page
        2. Enter unregistered email address
        3. Enter any password
        4. Click Login button
        5. Validate error message is displayed
        6. Validate user remains on login page
    """
    INVALID_EMAIL = "unregistered@example.com"
    PASSWORD = "AnyPass123!"
    # Instantiate the test page object
    tc_login_002 = TC_LOGIN_002_TestPage(driver)
    results = tc_login_002.run_tc_login_002(INVALID_EMAIL, PASSWORD)

    # Assert stepwise results
    assert results["step_1_navigate_login"] is True, f"Step 1 failed: Login page not displayed. Exception: {results['exception']}"
    assert results["step_2_enter_email"] is True, "Step 2 failed: Email not entered."
    assert results["step_3_enter_password"] is True, "Step 3 failed: Password not entered."
    assert results["step_4_click_login"] is True, "Step 4 failed: Login button not clicked."
    assert results["step_5_error_message"] is not None, "Step 5 failed: Error message not found."
    assert "invalid email or password" in results["step_5_error_message"].lower(), f"Step 5 failed: Unexpected error message: {results['step_5_error_message']}"
    assert results["step_6_on_login_page"] is True, "Step 6 failed: User is not on login page after failed login."
    assert results["overall_pass"] is True, f"Test failed overall. Exception: {results['exception']}"
