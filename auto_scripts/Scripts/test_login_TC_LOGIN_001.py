# Selenium Test Script for TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
LOGIN_URL = "https://example-ecommerce.com/login"
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "ValidPass123!"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.tc_id('TC_LOGIN_001')
def test_login_successful(driver):
    """
    Test Case TC_LOGIN_001: Valid Login
    Steps:
    1. Navigate to login page
    2. Verify login fields are visible
    3. Enter valid email
    4. Enter valid password
    5. Click Login
    6. Verify redirection and session
    """
    login_page = LoginPage(driver)

    # Step 2: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LOGIN_URL), "Should be on the login page URL"

    # Step 3: Login fields visible
    assert login_page.is_login_fields_visible(), "Email and Password fields should be visible"

    # Step 4: Enter valid email
    login_page.enter_credentials(VALID_EMAIL, VALID_PASSWORD)
    assert login_page.is_email_accepted(VALID_EMAIL), f"Email field should contain: {VALID_EMAIL}"

    # Step 5: Password masked
    assert login_page.is_password_masked(), "Password field should be masked (type='password')"

    # Step 6: Click Login
    login_page.click_login()

    # Step 7: Redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User should be redirected to dashboard and see profile icon"

    # Step 8: User authenticated and session token created
    assert login_page.is_user_authenticated(), "User profile icon should be displayed, indicating authentication"
    session_token = login_page.get_session_token()
    assert session_token is not None and len(session_token) > 0, "Session token should be present in cookies"
