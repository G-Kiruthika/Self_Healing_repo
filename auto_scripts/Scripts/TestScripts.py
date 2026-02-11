# Existing imports
from selenium import webdriver
import pytest
from auto_scripts.PageObjects.LoginPage import LoginPage
from auto_scripts.PageObjects.DashboardPage import DashboardPage

# Existing test functions...
# (Assume all previous code is preserved here)


def test_tc_login_001_valid_credentials():
    """
    TC_LOGIN_001: Valid Login
    Steps:
        1. Navigate to login page (https://ecommerce.example.com/login)
        2. Enter valid username (validuser@example.com)
        3. Enter valid password (ValidPass123!)
        4. Click Login
        5. Validate dashboard/home page displayed and session established
    """
    driver = webdriver.Chrome()
    try:
        driver.get("https://ecommerce.example.com/login")
        login_page = LoginPage(driver)
        login_page.enter_username("validuser@example.com")
        login_page.enter_password("ValidPass123!")
        login_page.click_login()

        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_displayed(), "Dashboard page was not displayed after login."
        assert dashboard_page.is_session_active(), "Session was not established after login."
    finally:
        driver.quit()
