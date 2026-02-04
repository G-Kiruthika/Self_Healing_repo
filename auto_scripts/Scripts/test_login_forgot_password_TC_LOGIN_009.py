# Test Script for TC_LOGIN_009: Forgot Password Link and Password Recovery Page
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

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

def test_forgot_password_link_and_recovery_page(driver):
    """
    TC_LOGIN_009:
    1. Navigate to the login page
    2. Verify 'Forgot Password' link is visible
    3. Click on the 'Forgot Password' link
    4. Verify redirection to password recovery page
    5. Verify password recovery page displays email input field and submit button
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    # Step 1: Login page is displayed with 'Forgot Password' link visible
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."
    assert login_page.is_forgot_password_link_visible(), "'Forgot Password' link is not visible on the login page."
    # Step 2: Click on the 'Forgot Password' link
    clicked = login_page.click_forgot_password_link()
    assert clicked, "Failed to click 'Forgot Password' link."
    # Step 3: Verify password recovery page elements
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_email_input_visible(), "Email input field is not visible on password recovery page."
    assert recovery_page.is_submit_button_visible(), "Submit button is not visible on password recovery page."
