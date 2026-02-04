# Test Script for TC_LOGIN_009: Forgot Password Navigation and UI Verification
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
import time

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_009_forgot_password_navigation_and_ui(driver):
    """
    TC_LOGIN_009:
    1. Navigate to the login page
    2. Click on the 'Forgot Password' link
    3. Verify password recovery page elements (email input and submit button)
    """
    # Step 1: Navigate to login page and check 'Forgot Password' link
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_forgot_password_link_visible(), "Forgot Password link is not visible on Login page."
    
    # Step 2: Click 'Forgot Password' link and verify redirection
    redirected = login_page.click_forgot_password_link()
    assert redirected, "Failed to click 'Forgot Password' link."
    time.sleep(2)  # Wait for navigation
    
    # Step 3: Verify password recovery page elements
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_loaded(), "Password Recovery page did not load."
    assert recovery_page.verify_page_elements(), "Password Recovery page does not display email input and submit button."
    
    # Optionally, print result
    print("TC_LOGIN_009 passed: Forgot Password navigation and UI verified.")
