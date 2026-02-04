# Test Script: test_login_negative_invalid_email.py
# Test Case: TC_LOGIN_002 - Invalid Email, Valid Password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_invalid_email_valid_password(driver):
    """
    TC_LOGIN_002: Attempt login with invalid email and valid password.
    Steps:
      1. Navigate to the login page
      2. Enter invalid email address
      3. Enter valid password (masked)
      4. Click on the Login button
      5. Verify error message and that user remains on login page
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible."
    # Step 2 & 3: Enter credentials
    invalid_email = "invaliduser@example.com"
    valid_password = "ValidPass123!"
    login_page.enter_credentials(invalid_email, valid_password)
    # Step 3: Password should be masked
    assert login_page.is_password_masked(), "Password field is not masked."
    # Step 4: Click login
    login_page.click_login()
    # Step 5: Error message is displayed
    assert login_page.is_error_message_displayed("Invalid email or password"), "Error message not displayed for invalid login."
    # Step 6: User remains on login page
    assert login_page.is_on_login_page(), "User is not on the login page after failed login."
