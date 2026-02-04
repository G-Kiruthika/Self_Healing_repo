# test_login_max_email_length.py
"""
Test Case: TC_LOGIN_011
Boundary test for login with maximum valid email length (254 characters)
Acceptance Criteria: SCRUM-91
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

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

def test_login_max_email_length(driver):
    """
    TC_LOGIN_011: Login with maximum email length (254 chars)
    Steps:
      1. Navigate to the login page
      2. Enter email address with 254 characters
      3. Enter valid password
      4. Click on the Login button
      5. Validate:
         - Email field accepts and displays the full value
         - Password field is masked
         - Login is processed (success if registered, error if not)
    """
    login_page = LoginPage(driver)
    max_length_email = (
        "a123456789012345678901234567890123456789012345678901234567890123@"
        "b123456789012345678901234567890123456789012345678901234567890123."
        "c123456789012345678901234567890123456789012345678901234567890123."
        "d123456789012345678901234567890123456789012345.com"
    )
    assert len(max_length_email) == 254, "Test email is not 254 chars!"
    valid_password = "ValidPass123!"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields not visible. [SCRUM-91]"

    # Step 2: Enter max length email
    assert login_page.enter_email(max_length_email), "Email not accepted in field. [SCRUM-91]"
    email_field = driver.find_element(*login_page.EMAIL_FIELD)
    actual_email = email_field.get_attribute("value")
    assert actual_email == max_length_email, "Email field does not display the full value. [SCRUM-91]"
    assert len(actual_email) == 254, f"Email field value length is {len(actual_email)}, expected 254. [SCRUM-91]"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password field not masked. [SCRUM-91]"
    password_field = driver.find_element(*login_page.PASSWORD_FIELD)
    assert password_field.get_attribute("type") == "password", "Password field not masked. [SCRUM-91]"

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(2)

    # Step 5: Validate login processed (success if registered, error if not)
    # Accept both outcomes: success (redirect to dashboard) or error message
    if login_page.is_redirected_to_dashboard():
        assert login_page.is_session_token_created(), "Session token not created after successful login. [SCRUM-91]"
        print("[PASS] Login successful with max-length email. [SCRUM-91]")
    elif login_page.is_error_message_displayed():
        print("[PASS] Error message displayed for unregistered max-length email. [SCRUM-91]")
    else:
        pytest.fail("Login outcome is unknown. Neither dashboard nor error message displayed. [SCRUM-91]")
