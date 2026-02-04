# Selenium Test Script for TC_LOGIN_013: SQL Injection on Login
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

# Import the LoginPage Page Object
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginSQLInjection(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode for CI
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        try:
            self.driver.quit()
        except WebDriverException:
            pass

    def test_sql_injection_login(self):
        """
        TC_LOGIN_013: Attempt login with SQL injection payload in email field.
        Steps:
        1. Navigate to the login page
        2. Enter SQL injection payload in email field
        3. Enter any password
        4. Click on the Login button
        Expected: Login fails with error message, SQL injection is prevented, no unauthorized access granted.
        Acceptance Criteria: SCRUM-91
        """
        sql_payload = "admin'--"
        password = "anything"

        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        self.assertEqual(self.driver.current_url, self.login_page.LOGIN_URL, "Login page URL mismatch.")
        self.assertTrue(self.login_page.is_login_fields_visible(), "Login fields not visible.")

        # Step 2: Enter SQL injection payload in email field
        email_entered = self.login_page.enter_email(sql_payload)
        self.assertTrue(email_entered, f"Email field did not accept payload: {sql_payload}")
        self.assertEqual(self.driver.find_element(*self.login_page.EMAIL_FIELD).get_attribute("value"), sql_payload, "Email input mismatch.")

        # Step 3: Enter password (should be masked)
        password_masked = self.login_page.enter_password(password)
        self.assertTrue(password_masked, "Password field is not masked.")
        self.assertEqual(self.driver.find_element(*self.login_page.PASSWORD_FIELD).get_attribute("type"), "password", "Password input not masked.")

        # Step 4: Click Login button
        self.login_page.click_login()
        time.sleep(2)  # Wait for response

        # Expected: Login fails, error message is displayed, SQL injection is prevented, no unauthorized access
        error_displayed = self.login_page.is_error_message_displayed()
        not_redirected = self.driver.current_url == self.login_page.LOGIN_URL
        unauthorized_access = not self.login_page.is_redirected_to_dashboard()

        self.assertTrue(error_displayed, "Error message not displayed for SQL injection attempt.")
        self.assertTrue(not_redirected, "User was redirected away from login page (possible unauthorized access).")
        self.assertTrue(unauthorized_access, "Unauthorized access granted after SQL injection attempt.")

if __name__ == "__main__":
    unittest.main()
