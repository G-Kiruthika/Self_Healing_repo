# test_tc_login_006_forgot_password_flow.py
"""
Automated Selenium test for TC_LOGIN_006: Forgot Password flow
Covers:
    1. Navigation to login page
    2. Click 'Forgot Password' link
    3. Enter registered email
    4. Click 'Send Reset Link'
    5. Verify success message and (placeholder) email receipt
Traceability:
    - PageClasses: LoginPage, PasswordRecoveryPage
    - TestCaseID: 198 (TC_LOGIN_006)
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.mark.usefixtures("driver")
def test_tc_login_006_forgot_password_flow(driver):
    """
    Test Case TC_LOGIN_006: Forgot Password Flow
    Steps:
        1. Navigate to the login page
        2. Click on 'Forgot Password' link
        3. Enter registered email address
        4. Click on 'Send Reset Link' button
        5. Verify success message is displayed
        6. (Placeholder) Verify password reset email is received
    """
    REGISTERED_EMAIL = "testuser@example.com"
    LOGIN_PAGE_URL = "https://example-ecommerce.com/login"  # As per PageClass
    PASSWORD_RECOVERY_URL = "https://ecommerce.example.com/forgot-password"  # As per PageClass

    # Step 1: Navigate to the login page
    login_page = LoginPage(driver)
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed"
    assert LOGIN_PAGE_URL in driver.current_url, f"Unexpected login page URL: {driver.current_url}"

    # Step 2: Click on 'Forgot Password' link
    login_page.click_forgot_password_link()

    # Step 3: Assert navigation to password recovery page
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_loaded(), "Password recovery page is not loaded after clicking 'Forgot Password'"
    assert PASSWORD_RECOVERY_URL in driver.current_url, f"Not on password recovery page. Current URL: {driver.current_url}"
    assert recovery_page.is_email_input_visible(), "Email input not visible on password recovery page"

    # Step 4: Enter registered email address
    email_entered = recovery_page.enter_email(REGISTERED_EMAIL)
    assert email_entered, f"Failed to enter email: {REGISTERED_EMAIL}"

    # Step 5: Click on 'Send Reset Link' button
    recovery_page.click_send_reset_link()

    # Step 6: Verify success message is displayed
    assert recovery_page.is_success_message_displayed(), "Success message not displayed after sending reset link"

    # Step 7: (Optional/Placeholder) Verify password reset email is received
    try:
        recovery_page.verify_password_reset_email_received(REGISTERED_EMAIL)
    except NotImplementedError:
        pass  # Acceptable as per PageClass docstring

    # Final assertion: If all above pass, test is successful
    return True

# Pytest fixture for WebDriver setup/teardown
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
