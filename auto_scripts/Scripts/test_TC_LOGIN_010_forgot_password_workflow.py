# Selenium Test Script for TC_LOGIN_010: Forgot Password Workflow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
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
class TestForgotPasswordWorkflow:
    """
    Test Case: TC_LOGIN_010
    Description: Validate forgot password workflow including UI flow and success message.
    Steps:
        1. Navigate to the password recovery page via Forgot Password link
        2. Enter registered email address
        3. Click on the Submit button
        4. Check email inbox for password reset link (external, placeholder)
    """

    @pytest.fixture(scope="function")
    def driver(self, request):
        driver = get_chrome_driver()
        yield driver
        driver.quit()

    def test_forgot_password_workflow(self, driver):
        EMAIL = "testuser@example.com"
        # Step 1: Navigate to password recovery via Forgot Password link
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        assert login_page.is_forgot_password_link_visible(), "Forgot Password link should be visible on login page."
        login_page.click_forgot_password_link()
        time.sleep(2)  # Wait for navigation
        # Step 2: Enter registered email address
        recovery_page = PasswordRecoveryPage(driver)
        assert recovery_page.is_loaded(), "Password recovery page should be loaded."
        assert recovery_page.is_email_input_visible(), "Email input should be visible on recovery page."
        assert recovery_page.enter_email(EMAIL), f"Email '{EMAIL}' was not entered correctly."
        # Step 3: Click on the Submit button
        assert recovery_page.is_submit_button_visible(), "Submit button should be visible on recovery page."
        recovery_page.submit_recovery()
        time.sleep(1)
        # Step 4: Check that success message is displayed
        assert recovery_page.is_success_message_displayed(), \
            "Success message 'Password reset link has been sent to your email' should be displayed."
        # Step 5: (External) Check email inbox for password reset link
        try:
            recovery_page.check_password_reset_email_received(EMAIL)
        except NotImplementedError:
            # Placeholder: Email inbox check must be implemented in test harness/CI pipeline
            pass
