# Selenium Test Script for TC_LOGIN_008: Login without 'Remember Me' and verify logout on browser restart
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pages')))
from LoginPage import LoginPage

class TestLoginWithoutRememberMe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.login_page = LoginPage(cls.driver)
        cls.valid_email = 'testuser@example.com'
        cls.valid_password = 'ValidPass123!'

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_TC_LOGIN_008_login_without_remember_me_and_verify_logout(self):
        """
        TC_LOGIN_008: Login with valid credentials and 'Remember Me' UNCHECKED, close and restart browser, verify user is logged out.
        Steps:
        1. Navigate to the login page
        2. Enter valid email and password
        3. Ensure 'Remember Me' checkbox is UNCHECKED
        4. Click Login button
        5. Close and restart browser, navigate to login page
        6. Assert user is logged out (redirected to login page)
        """
        driver = self.driver
        login_page = self.login_page

        # Step 1: Navigate to login page
        login_page.go_to_login_page()
        self.assertTrue(login_page.is_login_fields_visible(), "Login page is not displayed.")
        self.assertEqual(driver.current_url, LoginPage.LOGIN_URL, "Not on the login page URL.")

        # Step 2: Enter valid email and password
        email_entered = login_page.enter_email(self.valid_email)
        password_field_masked = login_page.enter_password(self.valid_password)
        self.assertTrue(email_entered, "Email was not entered correctly.")
        self.assertTrue(password_field_masked, "Password field is not masked.")

        # Step 3: Ensure 'Remember Me' checkbox is UNCHECKED
        checkbox = driver.find_element(*LoginPage.REMEMBER_ME_CHECKBOX)
        if checkbox.is_selected():
            checkbox.click()
        self.assertFalse(checkbox.is_selected(), "'Remember Me' checkbox should be unchecked.")

        # Step 4: Click Login button
        login_page.click_login()
        # Wait for redirect
        time.sleep(2)
        self.assertTrue(login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard after login.")
        self.assertTrue(login_page.is_session_token_created(), "Session token was not created after login.")

        # Step 5: Simulate closing and restarting browser by deleting all cookies and navigating to login page
        driver.delete_all_cookies()
        driver.get(LoginPage.LOGIN_URL)
        time.sleep(2)

        # Step 6: Assert user is logged out (redirected to login page)
        # User should NOT be redirected to dashboard, but remain on login page
        self.assertEqual(driver.current_url, LoginPage.LOGIN_URL, "User is not redirected to login page after browser restart.")
        # Optionally, check that login fields are visible again
        self.assertTrue(login_page.is_login_fields_visible(), "Login fields are not visible after browser restart.")

if __name__ == "__main__":
    unittest.main()
