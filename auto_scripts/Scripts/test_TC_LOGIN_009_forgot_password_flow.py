# Test Script for TC_LOGIN_009: Forgot Password Flow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_009_forgot_password_flow(driver):
    """
    Test Case TC_LOGIN_009
    1. Navigate to the login page
    2. Verify Forgot Password link is visible
    3. Click on the Forgot Password link
    4. Verify password recovery page is displayed
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Verify Forgot Password link is visible
    assert login_page.is_forgot_password_link_visible(), "Forgot Password link is not visible on the login page."

    # Step 3: Click on the Forgot Password link
    clicked = login_page.click_forgot_password_link()
    assert clicked, "Failed to click Forgot Password link."
    time.sleep(2)  # Wait for redirect

    # Step 4: Verify password recovery page is displayed
    recovery_page = PasswordRecoveryPage(driver)
    assert driver.current_url.startswith(PasswordRecoveryPage.PASSWORD_RECOVERY_URL), (
        f"Expected to be on password recovery page, got {driver.current_url}"
    )
    assert recovery_page.is_email_input_visible(), "Email input field is not visible on the password recovery page."
    assert recovery_page.is_submit_button_visible(), "Submit button is not visible on the password recovery page."
