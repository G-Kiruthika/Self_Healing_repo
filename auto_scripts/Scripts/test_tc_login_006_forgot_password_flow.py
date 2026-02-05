# test_tc_login_006_forgot_password_flow.py
"""
Automated Selenium Test Script for TC_LOGIN_006: Forgot Password Flow
Covers:
    1. Login page display
    2. Forgot Password navigation
    3. Email input and reset link submission
    4. Success message assertion
    5. (Placeholder) Email inbox assertion

Traceability:
    - PageClass: LoginPage, PasswordRecoveryPage
    - TestCase: TC_LOGIN_006
    - Steps mapped 1:1 to testCaseDescription
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.mark.usefixtures("setup")
class TestForgotPasswordFlow:
    def test_tc_login_006_forgot_password_flow(self):
        """
        TC_LOGIN_006: Forgot Password Flow
        Steps:
        1. Navigate to the login page
        2. Click on 'Forgot Password' link
        3. Enter registered email address
        4. Click on 'Send Reset Link' button
        5. Verify success message and password reset email
        """
        # --- Setup ---
        driver = self.driver
        login_page = LoginPage(driver)
        recovery_page = PasswordRecoveryPage(driver)
        registered_email = "testuser@example.com"

        # Step 1: Navigate to login page
        login_page.load()
        assert login_page.is_displayed(), "Login page is not displayed"

        # Step 2: Click on 'Forgot Password' link
        forgot_link = login_page.wait.until(
            lambda d: d.find_element(*login_page.FORGOT_PASSWORD_LINK)
        )
        forgot_link.click()

        # Step 3: Verify redirected to password recovery page
        assert recovery_page.is_loaded(), "Password Recovery page is not loaded after clicking 'Forgot Password'"
        assert recovery_page.is_email_input_visible(), "Email input not visible on Password Recovery page"

        # Step 4: Enter registered email and submit
        email_field = driver.find_element(*recovery_page.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(registered_email)
        submit_btn = driver.find_element(*recovery_page.SUBMIT_BUTTON)
        submit_btn.click()

        # Step 5: Verify success message
        success_msg = recovery_page.wait.until(
            lambda d: d.find_element(*recovery_page.SUCCESS_MESSAGE)
        )
        assert success_msg.is_displayed(), "Success message not displayed after submitting password reset"
        assert "Password reset link sent to your email" in success_msg.text, f"Unexpected success message: {success_msg.text}"

        # Step 6: (Optional/Placeholder) Verify password reset email received
        # This step requires integration with an email inbox or mock
        # Uncomment and implement if email inbox integration is available:
        # assert recovery_page.verify_password_reset_email_received(registered_email), "Password reset email not received in inbox"

        # Ensure no unexpected navigation
        assert recovery_page.PASSWORD_RECOVERY_URL in driver.current_url, "User was redirected away from recovery page unexpectedly"

# ---- Pytest fixture for Selenium WebDriver ----
@pytest.fixture(scope="class")
def setup(request):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    request.cls.driver = driver
    yield
    driver.quit()
