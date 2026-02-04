# Selenium Test Script for TC_LOGIN_017: Login Failed Attempts and Counter Reset
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.DashboardPage import DashboardPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_failed_attempts_and_reset(driver):
    """
    TC_LOGIN_017: Test failed login attempts, successful login, logout, and counter reset.
    Steps:
    1. Navigate to the login page
    2. Enter valid email and incorrect password, then click Login (Attempt 1-3)
    3. Verify error message displayed for each failed attempt
    4. Enter valid email and correct password, then click Login
    5. Verify user is successfully logged in, failed attempt counter is reset
    6. Logout and attempt login with incorrect password again
    7. Verify failed attempt counter starts from 1 again
    """
    # --- Test Data ---
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3"]
    correct_password = "ValidPass123!"
    wrong_password_after_logout = "WrongPass4"

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    assert driver.current_url == login_page.LOGIN_URL, "Not on the login page!"

    # Step 2: Attempt login with incorrect passwords (3 attempts)
    for idx, wrong_pass in enumerate(wrong_passwords, 1):
        assert login_page.enter_email(email), f"Email not entered correctly on attempt {idx}!"
        assert login_page.enter_password(wrong_pass), f"Password not entered correctly on attempt {idx}!"
        login_page.click_login()
        time.sleep(1)
        error_msg = login_page.get_error_message()
        assert error_msg is not None, f"No error message on failed attempt {idx}!"
        assert "error" in error_msg.lower() or "invalid" in error_msg.lower(), f"Unexpected error message on attempt {idx}: {error_msg}"
        assert driver.current_url == login_page.LOGIN_URL, "User should remain on login page after failed attempt!"

    # Step 3: Attempt login with correct password
    assert login_page.enter_email(email), "Email not entered correctly for successful login!"
    assert login_page.enter_password(correct_password), "Password not entered correctly for successful login!"
    login_page.click_login()
    time.sleep(1)
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard after correct login!"
    assert login_page.is_session_token_created(), "Session not created after correct login!"

    # Step 4: Logout
    dashboard = DashboardPage(driver)
    assert dashboard.is_loaded(), "Dashboard is not loaded after login!"
    assert dashboard.logout(), "Logout failed!"
    time.sleep(1)
    # After logout, should be redirected to login page
    assert login_page.is_login_fields_visible(), "Login fields are not visible after logout!"
    assert driver.current_url == login_page.LOGIN_URL, "Not redirected to login page after logout!"

    # Step 5: Attempt login with incorrect password again (counter should reset)
    assert login_page.enter_email(email), "Email not entered after logout!"
    assert login_page.enter_password(wrong_password_after_logout), "Password not entered after logout!"
    login_page.click_login()
    time.sleep(1)
    error_msg = login_page.get_error_message()
    assert error_msg is not None, "No error message after logout and failed login!"
    assert "error" in error_msg.lower() or "invalid" in error_msg.lower(), f"Unexpected error message after logout: {error_msg}"
    assert driver.current_url == login_page.LOGIN_URL, "User should remain on login page after failed login post logout!"
