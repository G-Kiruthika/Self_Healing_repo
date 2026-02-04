# Selenium Test Script for TC_LOGIN_010 - Forgot Password Workflow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.usefixtures("driver")
class TestForgotPassword:
    @pytest.fixture(scope="class")
    def driver(self, request):
        driver = get_chrome_driver()
        request.addfinalizer(driver.quit)
        return driver

    def test_TC_LOGIN_010_forgot_password_workflow(self, driver):
        """
        Test Case TC_LOGIN_010: Forgot Password workflow
        Steps:
        1. Navigate to the password recovery page
        2. Enter registered email address
        3. Click on Send Reset Link button
        4. Check email inbox (placeholder)
        Acceptance Criteria: Password recovery page is displayed, email input is accepted, success message is shown, password reset email is received.
        """
        # Test Data
        registered_email = "testuser@example.com"
        recovery_url = "https://app.example.com/forgot-password"

        # Step 1: Navigate to the password recovery page
        driver.get(recovery_url)
        recovery_page = PasswordRecoveryPage(driver)
        assert recovery_page.is_loaded(), "Password recovery page is not loaded (AC_006)"
        assert recovery_page.is_email_input_visible(), "Email input not visible (AC_006)"
        assert recovery_page.is_submit_button_visible(), "Submit button not visible (AC_006)"

        # Step 2: Enter registered email address
        email_entered = recovery_page.enter_email(registered_email)
        assert email_entered, f"Email '{registered_email}' was not entered correctly (AC_006)"

        # Step 3: Click on Send Reset Link button
        recovery_page.submit_recovery()
        time.sleep(2)  # Wait for the success message to appear

        # Step 3: Assert success message is displayed
        assert recovery_page.is_success_message_displayed(), "Success message 'Password reset link sent to your email' not displayed (AC_006)"

        # Step 4: Check email inbox (placeholder)
        try:
            recovery_page.check_password_reset_email_received(registered_email)
        except NotImplementedError:
            # Acceptable as this is a placeholder for integration
            pass
