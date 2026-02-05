# Test Script for TC-LOGIN-002: Invalid Login Attempt
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
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_002_invalid_login_flow(driver):
    """
    Test Case TC-LOGIN-002:
    1. Navigate to the login page
    2. Enter an unregistered or invalid email address
    3. Enter any password
    4. Click on the Login button
    5. Verify error message: 'Invalid email or password'
    6. Verify user remains on login page
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page is not displayed after navigation."

    # Step 2: Enter invalid email
    invalid_email = "invaliduser@example.com"
    assert login_page.enter_email(invalid_email), f"Email '{invalid_email}' was not entered correctly."

    # Step 3: Enter any password
    test_password = "SomePassword123"
    assert login_page.enter_password(test_password), "Password was not entered correctly or is not masked."

    # Step 4: Click Login
    assert login_page.click_login(), "Login button could not be clicked."

    # Step 5: Verify error message displayed
    assert login_page.is_error_message_displayed("Invalid email or password"), "Expected error message not displayed."

    # Step 6: Verify user remains on login page
    assert login_page.verify_user_stays_on_login_page(), "User did not remain on login page after invalid login."
