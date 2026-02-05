# Selenium Test Script for TC-LOGIN-002: Invalid Login Flow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_002_invalid_login_flow(driver):
    """
    TC-LOGIN-002: Attempt login with invalid/unregistered email and any password, expect error and remain on login page.
    Steps:
    1. Navigate to the login page
    2. Enter an unregistered or invalid email address
    3. Enter any password
    4. Click on the Login button
    5. Verify error message: 'Invalid email or password'
    6. Verify user remains on login page
    """
    login_page = LoginPage(driver)

    # Test Data
    email = "invaliduser@example.com"
    password = "SomePassword123"

    # Step 1: Navigate to login page
    login_page.navigate_to_login()
    assert login_page.is_login_page_displayed(), "Login page should be displayed."

    # Step 2: Enter invalid/unregistered email
    assert login_page.enter_email(email), f"Email '{email}' should be entered in the email field."

    # Step 3: Enter any password
    assert login_page.enter_password(password), "Password should be masked and entered."

    # Step 4: Click on Login button
    assert login_page.click_login(), "Login button should be clicked."

    # Step 5: Verify error message
    assert login_page.is_error_message_displayed("Invalid email or password"), (
        "Error message 'Invalid email or password' should be displayed."
    )

    # Step 6: Verify user remains on login page
    assert login_page.verify_user_stays_on_login_page(), (
        "User should not be authenticated and must remain on the login page."
    )
