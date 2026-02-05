'''
Selenium Automation Script for TC-LOGIN-007: Forgot Username Link Navigation
PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)

Test Case Reference:
- testCaseId: 234
- Description: Verify that clicking the 'Forgot Username' link on the login page redirects to the username recovery page and displays appropriate input fields and instructions.
- Acceptance Criteria: TS-005

Maintainer: Automation Team
'''

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_007_forgot_username_navigation(driver):
    """
    TC-LOGIN-007: Verify 'Forgot Username' link redirects to username recovery page.
    Steps:
    1. Navigate to the login page [https://ecommerce.example.com/login]
    2. Click on the 'Forgot Username' link
    3. Verify username recovery page is displayed [Expected URL: https://ecommerce.example.com/forgot-username]
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page_url = LoginPage.URL
    driver.get(login_page_url)
    wait = WebDriverWait(driver, 10)
    # Assert login page loaded and 'Forgot Username' link is present
    try:
        email_field = wait.until(EC.visibility_of_element_located(LoginPage.EMAIL_FIELD))
        assert email_field.is_displayed(), "Email field not displayed on login page."
        forgot_username_link = wait.until(EC.visibility_of_element_located(LoginPage.FORGOT_PASSWORD_LINK))
        assert forgot_username_link.is_displayed(), "'Forgot Username' link is not visible on login page."
    except TimeoutException:
        pytest.fail("Login page or 'Forgot Username' link did not load within timeout.")

    # Step 2: Click 'Forgot Username' link
    forgot_username_link.click()

    # Step 3: Verify redirect to username recovery page
    expected_url = "https://ecommerce.example.com/forgot-username"
    try:
        redirected = wait.until(lambda d: expected_url in d.current_url)
        assert redirected, f"Not redirected to username recovery page. Current URL: {driver.current_url}"
    except TimeoutException:
        pytest.fail(f"Redirection to username recovery page failed. Current URL: {driver.current_url}")
    # Verify presence of input fields and instructions (example locators, update as needed)
    try:
        # Example: Input for email/username recovery
        recovery_input = wait.until(EC.visibility_of_element_located((By.ID, "recovery-email")))
        assert recovery_input.is_displayed(), "Recovery input field not displayed."
        # Example: Instruction text
        instructions = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".recovery-instructions")))
        assert instructions.is_displayed(), "Recovery instructions not displayed."
    except TimeoutException:
        pytest.fail("Username recovery page elements not loaded or not found.")
