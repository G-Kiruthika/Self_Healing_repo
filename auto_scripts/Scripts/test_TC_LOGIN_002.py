# -*- coding: utf-8 -*-
"""
Test Script for TC_LOGIN_002: Negative Login Flow
Author: Enterprise Automation Bot
Description: Validates that incorrect password prevents login and displays error message.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

class TestLoginNegative:
    def test_login_with_incorrect_password(self, driver):
        """
        TC_LOGIN_002 Steps:
        1. Navigate to login page
        2. Enter valid registered email
        3. Enter incorrect password
        4. Click Login
        5. Verify user remains on login page
        """
        login_page = LoginPage(driver)
        # Step 1: Navigate to login page
        assert login_page.navigate_to_login(), "Login page is not displayed."
        # Step 2: Enter valid registered email
        email = "testuser@example.com"
        assert login_page.enter_email(email), f"Email '{email}' was not accepted."
        # Step 3: Enter incorrect password
        incorrect_password = "WrongPass456!"
        assert login_page.enter_incorrect_password(incorrect_password), "Password was not masked or not accepted."
        # Step 4: Click Login and check error message
        assert login_page.click_login_and_check_error(), "Error message 'Invalid email or password' not displayed."
        # Step 5: Verify user remains on login page
        assert login_page.verify_user_stays_on_login_page(), "User did not remain on login page after failed login."
