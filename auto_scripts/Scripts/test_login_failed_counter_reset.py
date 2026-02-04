# Selenium test script for TC_LOGIN_019: Login failed counter reset after successful login/logout
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure Pages folder is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

def driver_factory():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.login
@pytest.mark.tc_login_019
def test_login_failed_counter_reset_workflow():
    """
    Test Case TC_LOGIN_019:
    - Navigate to login page
    - Attempt login with two wrong passwords
    - Login with correct password
    - Logout
    - Attempt login with wrong password again
    - Verify failed counter reset (no warning about previous failures)
    """
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2"]
    correct_password = "ValidPass123!"
    wrong_password_after_logout = "WrongPass3"

    driver = driver_factory()
    try:
        login_page = LoginPage(driver)
        result = login_page.login_failed_counter_reset_workflow(
            email=email,
            wrong_passwords=wrong_passwords,
            correct_password=correct_password,
            wrong_password_after_logout=wrong_password_after_logout
        )
        assert result is True, "TC_LOGIN_019 failed: Counter did not reset or unexpected warning appeared."
    finally:
        try:
            driver.quit()
        except Exception:
            pass
