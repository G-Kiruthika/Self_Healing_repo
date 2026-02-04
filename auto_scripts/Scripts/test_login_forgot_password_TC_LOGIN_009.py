# Test Script for TC_LOGIN_009: Forgot Password Link and Password Recovery Page
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()

def test_TC_LOGIN_009_forgot_password_navigation_and_elements(driver):
    """
    TC_LOGIN_009:
    1. Navigate to the login page
    2. Verify 'Forgot Password' link is visible
    3. Click on the 'Forgot Password' link
    4. Verify redirection to password recovery page
    5. Verify password recovery page displays email input field and submit button
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    # Step 1: Login page is displayed with 'Forgot Password' link visible
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."
    assert login_page.is_forgot_password_link_visible(), "'Forgot Password' link is not visible on the login page."
    # Step 2: Click on the 'Forgot Password' link
    navigation_successful = login_page.go_to_forgot_password()
    assert navigation_successful, "Should be redirected to password recovery page after clicking 'Forgot Password'."
    # Step 3: Verify password recovery page elements
    time.sleep(2)
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_email_input_visible(), "Email input field is not visible on password recovery page."
    assert recovery_page.is_submit_button_visible(), "Submit button is not visible on password recovery page."
    assert recovery_page.verify_page_elements(), "Password recovery page should display both email input and submit button."
    # Optionally, check URL
    assert driver.current_url.startswith(recovery_page.PASSWORD_RECOVERY_URL), "Should be on password recovery page URL."
