# test_login_unverified_account.py
"""
Automated Selenium test for TC-LOGIN-015: Login attempt with unverified account
Traceability: TC-LOGIN-015, TS-013
PageClass: LoginPage (auto_scripts.Pages.LoginPage)

Best practices:
- Pytest framework
- Explicit waits
- Stepwise assertion and error handling
- Test data and expected values parameterized for maintainability
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

TEST_URL = "https://ecommerce.example.com/login"
UNVERIFIED_EMAIL = "unverified@example.com"
VALID_PASSWORD = "ValidPass123!"
EXPECTED_ERROR_MSG = "Please verify your email address before logging in."

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

@pytest.mark.tc_login_015
def test_login_unverified_account(driver):
    """
    Test Case TC-LOGIN-015: Login attempt with unverified account
    Steps:
      1. Navigate to the login page
      2. Enter email of an unverified account
      3. Enter correct password
      4. Click on the Login button
      5. Verify error message and authentication state
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_on_login_page(), "Login page is not displayed (Step 1)"

    # Step 2: Enter email of unverified account
    login_page.enter_email(UNVERIFIED_EMAIL)
    # Step 3: Enter correct password
    login_page.enter_password(VALID_PASSWORD)

    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Validate error message
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed (Step 4)"
    assert EXPECTED_ERROR_MSG in error_message, f"Expected error message not found. Got: {error_message}"

    # Step 6: Verify user is not authenticated (still on login page)
    assert login_page.is_on_login_page(), "User is not on login page after failed login (Step 5)"

    # Step 7: Verify option to resend verification email is visible
    try:
        resend_option = driver.find_element_by_xpath("//*[contains(text(), 'Resend verification email')]")
        assert resend_option.is_displayed(), "Resend verification email option is not visible (Step 5)"
    except Exception:
        pytest.fail("Resend verification email option not found (Step 5)")

    # Stepwise result dict (for traceability)
    results = login_page.run_tc_login_015_unverified_account(UNVERIFIED_EMAIL, VALID_PASSWORD)
    assert results["overall_pass"], f"PageClass workflow did not pass. Results: {results}"
