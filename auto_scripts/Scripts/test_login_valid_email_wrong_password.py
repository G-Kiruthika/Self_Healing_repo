# Test Script for TC-LOGIN-003: Valid Email + Wrong Password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data for TC-LOGIN-003
test_url = "https://example-ecommerce.com/login"
valid_email = "testuser@example.com"
wrong_password = "WrongPassword456"

@pytest.fixture(scope="module")
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
    1. Navigate to the login page
    2. Enter valid registered email address
    3. Enter incorrect password
    4. Click on the Login button
    5. Verify error message is displayed: 'Invalid email or password'
    6. Verify user remains on login page without authentication
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.navigate_to_login()
    assert login_page.is_login_page_displayed(), "Login page is not displayed."

    # Step 2: Enter valid registered email address
    email_entered = login_page.enter_email(valid_email)
    assert email_entered, f"Email '{valid_email}' was not entered correctly."

    # Step 3: Enter incorrect password
    password_entered = login_page.enter_password(wrong_password)
    assert password_entered, "Password was not entered or not masked."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify error message is displayed: 'Invalid email or password'
    error_displayed = login_page.is_error_message_displayed("Invalid email or password")
    assert error_displayed, "Expected error message 'Invalid email or password' was not displayed."

    # Step 6: Verify user remains on login page without authentication
    user_stays = login_page.verify_user_stays_on_login_page()
    assert user_stays, "User did not remain on login page; possible session created or redirect occurred."
