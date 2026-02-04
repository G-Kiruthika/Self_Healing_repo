# Selenium test script for TC_LOGIN_008: Login without Remember Me and verify logout on browser restart
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test data for TC_LOGIN_008
test_email = "testuser@example.com"
test_password = "ValidPass123!"

# This driver factory creates a new Chrome WebDriver instance
def driver_factory():
    options = Options()
    options.add_argument('--headless')  # Run headless for automation
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

@pytest.fixture(scope="function")
def driver():
    driver = driver_factory()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_without_remember_me_and_verify_logout_on_restart(driver):
    """
    TC_LOGIN_008: End-to-end test for login WITHOUT 'Remember Me' and verifying logout after browser restart.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter valid password
    4. Leave 'Remember Me' checkbox unchecked
    5. Click Login button
    6. Verify user is logged in and redirected to dashboard
    7. Save cookies, quit browser, start new browser
    8. Load cookies, navigate to app, verify user is logged out and redirected to login page
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    # Step 2: Enter valid email
    assert login_page.enter_email(test_email), "Email was not entered correctly!"
    # Step 3: Enter valid password
    assert login_page.enter_password(test_password), "Password was not entered/masked correctly!"
    # Step 4: Ensure Remember Me is unchecked
    assert login_page.uncheck_remember_me(), "Remember Me checkbox was not left unchecked!"
    # Step 5: Click Login button
    login_page.click_login()
    # Step 6: Verify user is redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
    assert login_page.is_session_token_created(), "User session was not created!"

    # Step 7: Save cookies and restart browser
    cookies = driver.get_cookies()
    driver.quit()
    new_driver = driver_factory()
    new_driver.implicitly_wait(10)
    new_driver.get(LoginPage.LOGIN_URL)
    for cookie in cookies:
        # Selenium requires domain to be set for add_cookie
        cookie_dict = cookie.copy()
        if 'sameSite' in cookie_dict:
            del cookie_dict['sameSite']
        if 'expiry' in cookie_dict and cookie_dict['expiry'] is not None and not isinstance(cookie_dict['expiry'], int):
            # Remove non-int expiry
            del cookie_dict['expiry']
        try:
            new_driver.add_cookie(cookie_dict)
        except Exception:
            pass  # Some cookies may not be settable, continue
    new_driver.get(LoginPage.LOGIN_URL)

    # Step 8: Verify user is logged out and redirected to login page
    try:
        email_field_visible = new_driver.find_element(*LoginPage.EMAIL_FIELD).is_displayed()
        password_field_visible = new_driver.find_element(*LoginPage.PASSWORD_FIELD).is_displayed()
        redirected_to_login = new_driver.current_url == LoginPage.LOGIN_URL
        assert email_field_visible, "Email field is not visible after browser restart!"
        assert password_field_visible, "Password field is not visible after browser restart!"
        assert redirected_to_login, f"User is not redirected to login page after restart! Current URL: {new_driver.current_url}"
    except Exception as e:
        new_driver.quit()
        pytest.fail(f"Failed to verify logout after browser restart: {e}")
    new_driver.quit()
