# Selenium Test Script for TC_LOGIN_016 (XSS payload in email field)
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
import time
import sys
import os

# Add Pages directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

class TestLoginXSSPayload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_login_with_xss_script_payload(self):
        """
        TC_LOGIN_016: Attempt login with XSS script payload in email field and verify input is sanitized or rejected and no script execution occurs.
        Steps:
        1. Navigate to the login page
        2. Enter XSS script payload in email field
        3. Enter any password
        4. Click on the Login button
        5. Verify no script execution
        Expected:
        - Input is sanitized or rejected
        - No alert popup or script execution occurs
        - System remains secure
        """
        email_xss_payload = "<script>alert('XSS')</script>@test.com"
        password = "TestPass123"

        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_login_fields_visible(), "Login fields are not visible!")
        self.assertTrue(self.login_page.enter_email(email_xss_payload), "XSS payload was not entered correctly!")
        self.assertTrue(self.login_page.enter_password(password), "Password was not entered/masked correctly!")
        self.login_page.click_login()
        time.sleep(1)  # Wait for possible error message or alert

        # Check that no JavaScript alert is triggered (no script execution)
        alert_present = False
        try:
            alert = self.driver.switch_to.alert
            _ = alert.text  # Access text to trigger exception if not present
            alert_present = True
        except Exception:
            alert_present = False
        self.assertFalse(alert_present, "Unexpected alert popup detected (possible XSS execution)!")

        # Check that input is sanitized or rejected (error message shown)
        error_message = self.login_page.get_error_message()
        self.assertIsNotNone(error_message, "No error message displayed for XSS payload!")
        self.assertTrue(
            "invalid" in error_message.lower() or "error" in error_message.lower() or "not allowed" in error_message.lower() or "sanitized" in error_message.lower(),
            f"Unexpected error message: {error_message}"
        )
        self.assertEqual(self.driver.current_url, self.login_page.LOGIN_URL, "User is not on login page after XSS payload!")
        # Ensure system remains secure (no redirection, no script execution)
        self.assertFalse(self.login_page.is_redirected_to_dashboard(), "Unauthorized access granted after XSS payload!")

if __name__ == "__main__":
    unittest.main()
