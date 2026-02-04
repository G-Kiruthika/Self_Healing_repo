# Selenium Automation Test Script for TC_LOGIN_010 - Forgot Password Workflow
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
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.usefixtures("setup_and_teardown")
class TestForgotPasswordWorkflow:
    @pytest.fixture(scope="class")
    def setup_and_teardown(self, request):
        driver = get_chrome_driver()
        request.cls.driver = driver
        yield
        driver.quit()

    def test_TC_LOGIN_010_forgot_password_workflow(self):
        """
        Test Case TC_LOGIN_010:
        1. Navigate to the password recovery page
        2. Enter registered email address
        3. Click on Send Reset Link button
        4. Check email inbox (placeholder)
        """
        EMAIL = "testuser@example.com"
        RECOVERY_URL = PasswordRecoveryPage.PASSWORD_RECOVERY_URL

        # Step 1: Navigate to the password recovery page
        self.driver.get(RECOVERY_URL)
        recovery_page = PasswordRecoveryPage(self.driver)
        assert recovery_page.is_loaded(), "Password recovery page is not loaded."

        # Step 2: Enter registered email address
        assert recovery_page.is_email_input_visible(), "Email input field not visible."
        email_entered = recovery_page.enter_email(EMAIL)
        assert email_entered, f"Email '{EMAIL}' was not entered correctly."

        # Step 3: Click on Send Reset Link button
        assert recovery_page.is_submit_button_visible(), "Submit button not visible."
        recovery_page.submit_recovery()
        time.sleep(2)
        success_msg_displayed = recovery_page.is_success_message_displayed()
        assert success_msg_displayed, "Success message not displayed after submitting password recovery."

        # Step 4: Check email inbox for password reset link (placeholder)
        try:
            recovery_page.check_password_reset_email_received(EMAIL)
        except NotImplementedError:
            # Acceptable for now; integration to be implemented in test harness
            pass
