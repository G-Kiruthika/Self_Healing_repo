# Test Script for TC_LOGIN_009: Forgot Password Link and Recovery Page Validation
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.usefixtures("driver")
class TestForgotPassword:
    def test_forgot_password_link_and_recovery_page(self):
        """
        TC_LOGIN_009:
        1. Navigate to the login page
        2. Verify 'Forgot Password' link is visible
        3. Click the link and verify redirection to password recovery page
        4. Verify password recovery page displays email input and submit button
        """
        driver = get_chrome_driver()
        try:
            # Step 1: Navigate to login page
            login_page = LoginPage(driver)
            login_page.go_to_login_page()
            assert driver.current_url.startswith(LoginPage.LOGIN_URL), f"Current URL {driver.current_url} does not match login page!"

            # Step 2: Verify 'Forgot Password' link is visible
            assert login_page.is_forgot_password_link_visible(), "'Forgot Password' link is not visible on the login page!"

            # Step 3: Click the link and verify redirection
            clicked = login_page.click_forgot_password_link()
            assert clicked, "Failed to click 'Forgot Password' link!"
            time.sleep(1)  # Allow page to load

            # Step 4: Verify password recovery page elements
            recovery_page = PasswordRecoveryPage(driver)
            assert recovery_page.is_loaded(), "Password recovery page did not load properly!"
            assert recovery_page.verify_page_elements(), "Recovery page elements (email input and submit button) are not visible!"
        finally:
            driver.quit()
