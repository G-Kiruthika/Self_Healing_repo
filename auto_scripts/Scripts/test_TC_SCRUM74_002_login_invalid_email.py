# Test Script for TC_SCRUM74_002: Invalid Email Format Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
test_url = "https://app.example.com/login"
invalid_email = "invalidemail@"
valid_password = "ValidPass123!"
expected_error = "Invalid email or username"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.tc_id("TC_SCRUM74_002")
def test_login_with_invalid_email_format(driver):
    """
    Test Case TC_SCRUM74_002: Attempt login with invalid email format and verify error message.
    Steps:
    1. Navigate to the login page
    2. Enter invalid email format
    3. Enter valid password
    4. Click Login and verify error message
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page did not load correctly."
    assert driver.current_url.startswith(test_url), f"Unexpected URL after navigation: {driver.current_url}"

    # Step 2: Enter invalid email format
    assert login_page.enter_invalid_email_format(invalid_email), "Invalid email was not accepted in the field."
    email_value = driver.find_element(*LoginPage.EMAIL_INPUT).get_attribute("value")
    assert email_value == invalid_email, f"Email input value mismatch: got '{email_value}'"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Valid password was not accepted or not masked."
    password_type = driver.find_element(*LoginPage.PASSWORD_INPUT).get_attribute("type")
    assert password_type == "password", "Password field is not masked."

    # Step 4: Click Login and verify error message
    result = login_page.click_login_and_check_invalid_email_error()
    assert result, f"Expected error message '{expected_error}' was not displayed."
    error_elem = driver.find_element(*LoginPage.ERROR_MESSAGE)
    assert error_elem.is_displayed(), "Error message element is not visible."
    assert expected_error in error_elem.text, f"Error message text mismatch: got '{error_elem.text}'"
