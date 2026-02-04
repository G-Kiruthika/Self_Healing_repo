# Test Script for TC_LOGIN_013: Login with Maximum Length Password (128 characters)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
import time

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

def test_login_with_max_length_password_tc_login_013(driver):
    """
    Test Case TC_LOGIN_013 - Enter valid email and maximum allowed password (128 characters), click Login, verify acceptance and no validation error.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_007]
    2. Enter valid email address [Test Data: Email: testuser@example.com] [Acceptance Criteria: AC_007]
    3. Enter password at maximum allowed length (128 characters) [Test Data: Password: Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!]
    4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: AC_007]
    5. Login attempt is processed without validation error
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    password = "Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!"
    assert len(password) == 128, f"Password length is not 128, got {len(password)}"
    
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL is incorrect!"
    
    # Step 2: Verify login fields are visible
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    
    # Step 3: Enter valid email
    assert login_page.enter_email(email), "Email was not entered correctly!"
    
    # Step 4: Enter 128-char password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"
    
    # Step 5: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for any error or validation
    
    # Step 6: Check for validation or error messages
    error_message = login_page.get_error_message()
    validation_error = None
    try:
        validation_error = driver.find_element(*login_page.VALIDATION_ERROR)
        if validation_error.is_displayed():
            pytest.fail(f"Validation error shown: {validation_error.text}")
    except NoSuchElementException:
        pass
    assert not error_message, f"Unexpected error message: {error_message}"
