# Test Script for TC_LOGIN_017: Account lock after multiple failed login attempts
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.mark.usefixtures('driver_init')
class TestLoginAccountLock:
    """
    Test Case: TC_LOGIN_017
    Title: Account lock after multiple failed login attempts
    Steps:
      1. Navigate to the login page
      2. Enter valid email address
      3. Enter incorrect password and attempt login (Attempt 1)
      4. Repeat login with incorrect password (Attempts 2-5)
      5. After 5th failed attempt, verify account is locked and error message is displayed
      6. Attempt login with correct password, verify login is prevented (account remains locked)
    """

    @pytest.fixture(scope="class")
    def driver_init(self, request):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        request.cls.driver = driver
        yield
        driver.quit()

    def test_account_lock_after_failed_logins(self):
        # Test Data
        email = "testuser@example.com"
        wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
        correct_password = "ValidPass123!"

        login_page = LoginPage(self.driver)

        # Step 1: Navigate to the login page
        login_page.go_to_login_page()
        assert login_page.is_login_fields_visible(), "Login fields are not visible!"
        
        # Step 2: Enter valid email address
        assert login_page.enter_email(email), "Email was not entered correctly!"
        
        # Steps 3-5: Enter incorrect passwords and attempt login (5 times)
        for idx, pwd in enumerate(wrong_passwords):
            assert login_page.enter_password(pwd), f"Password was not entered correctly for attempt {idx+1}!"
            login_page.click_login()
            time.sleep(1)  # Wait for error message
            error_message = login_page.get_error_message()
            assert error_message is not None, f"No error message displayed for failed attempt {idx+1}!"
            if idx < 4:
                assert "incorrect" in error_message.lower(), f"Unexpected error message for attempt {idx+1}: {error_message}"
            else:
                assert "account locked" in error_message.lower(), f"Account lock message not displayed after 5th attempt: {error_message}"
        
        # Step 6: Attempt login with correct password (should remain locked)
        assert login_page.enter_password(correct_password), "Correct password not entered after lock!"
        login_page.click_login()
        time.sleep(1)
        error_message = login_page.get_error_message()
        assert error_message is not None, "No error message displayed after attempting login post-lock!"
        assert "account locked" in error_message.lower(), f"Account remains locked error not displayed: {error_message}"
        
        print("TC_LOGIN_017 passed: Account lock workflow verified.")
