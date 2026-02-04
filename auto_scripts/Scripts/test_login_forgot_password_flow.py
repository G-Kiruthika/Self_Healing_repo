# Selenium Test Script for TC_LOGIN_009 - Forgot Password Flow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

def driver_factory():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.usefixtures('driver')
class TestForgotPassword:
    def test_tc_login_009_forgot_password_navigation(self):
        """
        TC_LOGIN_009: Forgot Password link navigation and password recovery page element verification.
        Steps:
        1. Navigate to the login page
        2. Verify 'Forgot Password' link is visible
        3. Click the 'Forgot Password' link
        4. Verify redirection to password recovery page
        5. Verify password recovery page displays email input field and submit button
        """
        driver = driver_factory()
        try:
            login_page = LoginPage(driver)
            # Step 1: Navigate to login page
            login_page.go_to_login_page()
            assert driver.current_url.startswith(LoginPage.LOGIN_URL), f"Not on Login page, URL: {driver.current_url}"
            # Step 2: Verify 'Forgot Password' link is visible
            assert login_page.is_forgot_password_link_visible(), "Forgot Password link is not visible!"
            # Step 3: Click the 'Forgot Password' link
            login_page.click_forgot_password_link()
            # Step 4: Instantiate PasswordRecoveryPage and verify elements
            recovery_page = PasswordRecoveryPage(driver)
            assert recovery_page.is_loaded(), "Password recovery page is not loaded!"
            # Step 5: Verify password recovery page displays email input field and submit button
            assert recovery_page.verify_page_elements(), "Password recovery page elements are not visible!"
        finally:
            driver.quit()
