# Test Script for TC_LOGIN_010: Forgot Password Workflow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
import time

@pytest.mark.usefixtures("setup")
class TestForgotPassword:
    """
    Automated Selenium test for TC_LOGIN_010:
    1. Navigate to password recovery via Forgot Password link
    2. Enter registered email address
    3. Click Send Reset Link
    4. Check for success message
    5. (Optionally) Check email inbox for reset link (requires external integration)
    """
    def test_forgot_password_workflow(self, driver):
        # Test Data
        recovery_url = "https://app.example.com/forgot-password"
        registered_email = "testuser@example.com"

        # Step 1: Navigate to the password recovery page via Forgot Password link
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        assert login_page.is_forgot_password_link_visible(), "Forgot Password link not visible on login page."
        login_page.click_forgot_password_link()
        time.sleep(2)  # Wait for navigation
        assert driver.current_url.startswith(recovery_url), f"Expected to be on password recovery page, got {driver.current_url}"

        # Step 2: Enter registered email address
        recovery_page = PasswordRecoveryPage(driver)
        assert recovery_page.is_loaded(), "Password recovery page did not load properly."
        assert recovery_page.is_email_input_visible(), "Email input not visible on recovery page."
        entered = recovery_page.enter_email(registered_email)
        assert entered, "Email was not entered correctly in the recovery form."

        # Step 3: Click on Send Reset Link button
        assert recovery_page.is_submit_button_visible(), "Submit button not visible on recovery page."
        recovery_page.submit_recovery()
        time.sleep(1)  # Wait for response

        # Step 4: Assert success message is displayed
        assert recovery_page.is_success_message_displayed(), "Success message not displayed after password recovery."

        # Step 5: (Optional/Manual) Check email inbox for reset link
        # This requires integration with an email service or mock inbox
        # Uncomment and implement if infrastructure is available
        # assert recovery_page.check_password_reset_email_received(registered_email), "Password reset email not received."

# --- Pytest fixture for Selenium WebDriver setup and teardown ---
@pytest.fixture(scope="function")
def setup(request):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()
