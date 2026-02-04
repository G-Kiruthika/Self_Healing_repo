# Selenium Test Script for TC_LOGIN_008: Login without 'Remember Me' and verify logout after browser restart
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

def driver_factory():
    # You may replace this with your own driver setup as needed
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver

@pytest.mark.usefixtures("setup")
class TestLoginWithoutRememberMe:
    """
    Test Case TC_LOGIN_008
    Steps:
        1. Navigate to the login page
        2. Enter valid email and password
        3. Leave 'Remember Me' checkbox unchecked
        4. Click Login button
        5. Close and restart the browser, then navigate to the application
    Acceptance Criteria: After browser restart, user is logged out and redirected to login page.
    """
    def test_login_without_remember_me_logout_on_restart(self):
        email = "testuser@example.com"
        password = "ValidPass123!"
        driver = driver_factory()
        try:
            login_page = LoginPage(driver)
            # Step 1: Navigate to login page
            login_page.go_to_login_page()
            assert login_page.is_login_fields_visible(), "Login fields are not visible!"
            # Step 2: Enter valid email and password
            assert login_page.enter_email(email), "Email was not entered correctly!"
            assert login_page.enter_password(password), "Password was not entered/masked correctly!"
            # Step 3: Leave 'Remember Me' unchecked
            assert login_page.uncheck_remember_me(), "Remember Me checkbox was not left unchecked!"
            # Step 4: Click Login button
            login_page.click_login()
            # Wait for redirection
            time.sleep(1)
            assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard!"
            assert login_page.is_session_token_created(), "User session was not created!"
            # Step 5: Save cookies, quit browser, restart
            cookies = driver.get_cookies()
            driver.quit()
            new_driver = driver_factory()
            new_driver.get(LoginPage.LOGIN_URL)
            for cookie in cookies:
                # Selenium requires domain for add_cookie; skip cookies without domain
                if 'domain' in cookie:
                    try:
                        new_driver.add_cookie(cookie)
                    except Exception:
                        pass
            new_driver.get(LoginPage.LOGIN_URL)
            # After restart: Should be redirected to login page (not dashboard)
            try:
                login_fields_visible = (
                    new_driver.find_element(*LoginPage.EMAIL_FIELD).is_displayed() and
                    new_driver.find_element(*LoginPage.PASSWORD_FIELD).is_displayed()
                )
                redirected_to_login = new_driver.current_url == LoginPage.LOGIN_URL
                assert login_fields_visible and redirected_to_login, "User is NOT logged out after browser restart!"
            finally:
                new_driver.quit()
        finally:
            # Ensure original driver is closed if not already
            try:
                driver.quit()
            except Exception:
                pass
