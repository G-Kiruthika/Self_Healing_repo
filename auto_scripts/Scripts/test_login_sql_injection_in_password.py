# Selenium test script for TC_LOGIN_015: SQL Injection in Password Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
import time

from auto_scripts.Pages.LoginPage import LoginPage

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.security
@pytest.mark.login
@pytest.mark.parametrize("email, sql_payload", [
    ("testuser@example.com", "' OR '1'='1")
])
def test_login_with_sql_injection_in_password(email, sql_payload):
    """
    TC_LOGIN_015: Attempt login with valid email and SQL injection payload in password field.
    Acceptance Criteria: SCRUM-91
    Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Enter SQL injection payload in password field
        4. Click on the Login button
        5. Assert:
            - Input is masked and entered
            - Login fails with error message
            - SQL injection is prevented
            - No unauthorized access
    """
    driver = get_chrome_driver()
    try:
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        # Step 1: Assert login page is displayed
        assert login_page.is_login_fields_visible(), "Login fields are not visible."
        assert driver.current_url.startswith(LoginPage.LOGIN_URL), f"Not on login page: {driver.current_url}"

        # Step 2: Enter valid email
        email_accepted = login_page.enter_email(email)
        assert email_accepted, f"Email '{email}' was not accepted in email field."
        email_field = driver.find_element(*LoginPage.EMAIL_FIELD)
        assert email_field.get_attribute("value") == email, "Email field value mismatch."

        # Step 3: Enter SQL injection payload as password
        password_masked = login_page.enter_password(sql_payload)
        assert password_masked, "Password field is not masked (should be type='password')."
        password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
        assert password_field.get_attribute("type") == "password", "Password field is not masked."
        assert password_field.get_attribute("value") == sql_payload, "Password payload was not entered correctly."

        # Step 4: Click Login
        login_page.click_login()

        # Step 5: Assert login fails, error message shown, SQLi prevented, not redirected
        time.sleep(1.5)  # Wait for error message
        error_displayed = login_page.is_error_message_displayed()
        assert error_displayed, "Error message not displayed after SQL injection attempt."
        still_on_login_page = driver.current_url == LoginPage.LOGIN_URL
        assert still_on_login_page, f"User was redirected unexpectedly: {driver.current_url}"
        unauthorized_access = not login_page.is_redirected_to_dashboard()
        assert unauthorized_access, "User was redirected to dashboard (unauthorized access)."

        # Extra: Ensure no alert popup (XSS/SQLi prevention)
        alert_triggered = False
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            alert_triggered = True
        except NoAlertPresentException:
            pass
        except Exception:
            pass
        assert not alert_triggered, "Unexpected alert triggered (potential XSS/SQLi)."
    finally:
        driver.quit()
