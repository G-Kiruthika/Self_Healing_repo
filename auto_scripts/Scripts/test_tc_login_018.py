# test_tc_login_018.py
"""
Test Case: TC_LOGIN_018 - Multiple Failed Login Attempts & Warning Message
Author: Automation Generator
Traceability:
    - PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)
    - TestCaseId: 155
    - Test Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Attempt login with incorrect password three times
        4. Verify warning message after third attempt
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
LOGIN_URL = "https://app.example.com/login"
VALID_EMAIL = "testuser@example.com"
INVALID_PASSWORDS = ["WrongPass1", "WrongPass2", "WrongPass3"]
EXPECTED_WARNING = "Warning: Account will be locked after 2 more failed attempts"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.tc_id_155
@pytest.mark.login
def test_tc_login_018_multiple_failed_attempts(driver):
    """
    TC_LOGIN_018: Attempt login with incorrect password three times and verify warning message.
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_on_login_page(), "Login page should be displayed (Step 1)"

    # Step 2: Enter valid email address
    login_page.enter_email(VALID_EMAIL)
    # No explicit assert since field entry is covered in PageClass

    # Step 3: Attempt login with incorrect passwords three times
    for idx, pwd in enumerate(INVALID_PASSWORDS):
        login_page.enter_password(pwd)
        login_page.click_login()
        error_msg = login_page.get_error_message()
        assert error_msg is not None, f"Error message should be displayed after failed attempt {idx+1} (Step 3)"

    # Step 4: Verify warning message after third attempt
    warning_elem = driver.find_element(*LoginPage.WARNING_MESSAGE)
    assert warning_elem.is_displayed(), "Warning message should be displayed after three failed attempts (Step 4)"
    assert warning_elem.text.strip() == EXPECTED_WARNING, (
        f"Expected warning message '{EXPECTED_WARNING}', got '{warning_elem.text.strip()}' (Step 4)"
    )

    # Traceability: Store PageClass method output for audit (optional, not required by test)
    results = login_page.run_tc_login_018(VALID_EMAIL, INVALID_PASSWORDS)
    assert results['overall_pass'], f"PageClass run_tc_login_018() validation failed: {results}"
