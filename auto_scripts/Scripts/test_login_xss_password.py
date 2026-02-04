# Test Script for TC_LOGIN_014: Attempt login with XSS script in password field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')  # Comment this if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_xss_password(driver):
    """
    TC_LOGIN_014: Attempt login with valid email and XSS script payload in password field.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email address [Test Data: Email: testuser@example.com]
    3. Enter XSS script payload in password field [Test Data: Password: <script>alert('XSS')</script>]
    4. Click on the Login button
    Acceptance Criteria: SCRUM-91
    Expected: Input is masked and entered. Login fails safely, script is not executed, XSS attack is prevented.
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    xss_password = "<script>alert('XSS')</script>"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch"
    assert login_page.is_login_fields_visible(), "Login fields are not visible"

    # Step 2: Enter valid email
    assert login_page.enter_email(email), "Email input failed or not accepted"
    email_field = driver.find_element(*LoginPage.EMAIL_FIELD)
    assert email_field.get_attribute("value") == email, "Email not set in the input field"

    # Step 3: Enter XSS payload in password field
    assert login_page.enter_password(xss_password), "Password input is not masked or not accepted"
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_field.get_attribute("type") == "password", "Password field is not masked"
    assert password_field.get_attribute("value") == xss_password, "XSS payload not set in password field"

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(1)  # Allow for any error messages or redirects

    # Check error message is displayed
    assert login_page.is_error_message_displayed(), "Error message not displayed after XSS password attempt"
    # Ensure user is still on login page (not redirected)
    assert driver.current_url == LoginPage.LOGIN_URL, "User was redirected from login page after XSS password attempt"
    # Ensure no unauthorized access
    assert not login_page.is_redirected_to_dashboard(), "User was redirected to dashboard after XSS password attempt"

    # Ensure no browser alert is triggered (XSS not executed)
    alert_present = False
    try:
        driver.switch_to.alert
        alert_present = True
    except NoAlertPresentException:
        alert_present = False
    except Exception:
        alert_present = False
    assert not alert_present, "Browser alert was triggered (possible XSS execution)"
