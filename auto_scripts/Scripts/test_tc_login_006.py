# test_tc_login_006.py
"""
Automated Selenium test for TC-LOGIN-006: Forgot Password navigation and recovery page display.

Test Steps:
1. Navigate to the login page.
2. Click on the 'Forgot Password' link.
3. Verify password recovery page is displayed.

Traceability:
- Page Objects: LoginPage, PasswordRecoveryPage
- Test Case: TC-LOGIN-006
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_006_forgot_password_navigation(driver):
    """
    TC-LOGIN-006: Verify navigation to password recovery page via 'Forgot Password' link.
    """
    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed"

    # Step 2: Assert 'Forgot Password' link is present and clickable, then click
    try:
        forgot_link = driver.find_element(*LoginPage.FORGOT_PASSWORD_LINK)
        assert forgot_link.is_displayed(), "'Forgot Password' link is not visible on Login page"
    except Exception as e:
        pytest.fail(f"'Forgot Password' link not found: {e}")

    login_page.click_forgot_password_link()

    # Step 3: Verify navigation to password recovery page
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_loaded(), (
        f"Password Recovery page is not loaded. Current URL: {driver.current_url}"
    )
    # Check for email input and instructions
    assert recovery_page.is_email_input_visible(), "Email input is not visible on Password Recovery page"
    # Optionally, check for presence of instructions div
    instructions = driver.find_elements_by_css_selector('div.instructions')
    if instructions:
        assert instructions[0].is_displayed(), "Instructions are not visible on Password Recovery page"
