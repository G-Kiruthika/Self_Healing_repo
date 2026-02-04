# test_login_failed_counter_reset.py
"""
Selenium Automation Test Script for TC_LOGIN_019: Failed Login Attempts Counter Reset
Author: Automation Agent
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope='function')
def driver_factory():
    def factory():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        return webdriver.Chrome(options=options)
    return factory


def test_login_failed_counter_reset(driver, driver_factory):
    """
    Test Case: TC_LOGIN_019
    Objective: Verify failed login attempts counter is reset after successful login and logout.
    Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Attempt login with incorrect password twice
        4. Enter correct password and login
        5. Logout and attempt login with incorrect password
        6. Verify failed attempt counter is reset and no warning about previous failures
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2"]
    correct_password = "ValidPass123!"
    wrong_password_after_logout = "WrongPass3"
    result = login_page.login_failed_counter_reset(
        email=email,
        wrong_passwords=wrong_passwords,
        correct_password=correct_password,
        wrong_password_after_logout=wrong_password_after_logout
    )
    assert result is True, "Failed login attempts counter did not reset as expected."
