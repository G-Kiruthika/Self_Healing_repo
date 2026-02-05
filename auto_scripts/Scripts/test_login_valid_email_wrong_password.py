# Test script for TC-LOGIN-003: Login with valid email and incorrect password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_003_valid_email_wrong_password(driver):
    """
    TC-LOGIN-003: Login attempt with valid registered email and incorrect password
    Steps:
    1. Navigate to the login page [Test Data: URL]
    2. Enter valid registered email address [Test Data: Email]
    3. Enter incorrect password [Test Data: Password]
    4. Click on the Login button
    5. Verify error message displayed: 'Invalid email or password'
    6. Verify user remains on login page without authentication
    Acceptance Criteria: TS-002
    """
    login_page = LoginPage(driver)
    url = "https://ecommerce.example.com/login"
    email = "testuser@example.com"
    password = "WrongPassword456"
    expected_error = "Invalid email or password"

    # Step 1: Navigate to the login page
    driver.get(url)
    assert login_page.is_login_page_displayed(), "Login page is not displayed"

    # Step 2: Enter valid registered email address
    assert login_page.enter_email(email), f"Email '{email}' was not entered correctly"

    # Step 3: Enter incorrect password
    assert login_page.enter_password(password), f"Password was not entered or not masked"

    # Step 4: Click on the Login button
    assert login_page.click_login(), "Failed to click Login button"

    # Step 5: Verify error message is displayed
    assert login_page.is_error_message_displayed(expected_error), f"Expected error message '{expected_error}' not displayed"

    # Step 6: Verify user remains on login page without authentication
    assert login_page.verify_user_stays_on_login_page(), "User did not remain on login page, or session was created"
