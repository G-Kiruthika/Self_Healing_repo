# -*- coding: utf-8 -*-
"""
Selenium Automation Test Script for TC_LOGIN_018: Account Lockout Warning
Author: Enterprise Automation Agent
Date: 2024-06
Traceability: PageClass=LoginPage, TestCaseId=148, TestCase=TC_LOGIN_018
"""
import pytest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.mark.usefixtures("driver_init")
class TestLoginAccountLockoutWarning:
    def test_account_lockout_warning(self, driver):
        """
        TC_LOGIN_018: Test failed login attempts and verify lockout warning messages.
        Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter valid email and incorrect password, click Login (Attempts 1-2)
        3. Attempt login with incorrect password for the 3rd time
        4. Attempt login with incorrect password for the 4th time
        Expected:
        - Error message with warning about account lockout is displayed at 3rd and 4th attempts
        """
        login_page = LoginPage(driver)
        email = "testuser@example.com"
        wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4"]
        login_page.go_to_login_page()
        assert login_page.is_login_fields_visible(), "Login fields are not visible!"
        for attempt, wrong_password in enumerate(wrong_passwords, 1):
            assert login_page.enter_email(email), f"Email was not entered correctly for attempt {attempt}!"
            assert login_page.enter_password(wrong_password), f"Wrong password was not entered correctly for attempt {attempt}!"
            login_page.click_login()
            time.sleep(1)  # Wait for error message
            error_message = login_page.get_error_message()
            assert error_message is not None, f"No error message displayed for attempt {attempt}!"
            if attempt <= 2:
                assert "invalid credentials" in error_message.lower() or "invalid email or password" in error_message.lower(), f"Unexpected error message at attempt {attempt}: {error_message}"
            elif attempt == 3:
                assert "invalid credentials" in error_message.lower(), f"Expected 'Invalid credentials' in error message at attempt 3, got: {error_message}"
                assert "2 more attempts before your account is locked" in error_message.lower(), f"Expected warning about 2 attempts left at attempt 3, got: {error_message}"
            elif attempt == 4:
                assert "invalid credentials" in error_message.lower(), f"Expected 'Invalid credentials' in error message at attempt 4, got: {error_message}"
                assert "1 more attempt before your account is locked" in error_message.lower(), f"Expected warning about 1 attempt left at attempt 4, got: {error_message}"
            assert driver.current_url == login_page.LOGIN_URL, f"User is not on login page after failed attempt {attempt}!"
