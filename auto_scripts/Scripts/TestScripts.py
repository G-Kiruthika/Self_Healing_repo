# Existing content of TestScripts.py
# ... (existing test methods)
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...
    ...
    def test_tc_login_06_empty_email_and_password_error(self):
        ...
    def test_tc_login_07_remember_me_session_persistence(self):
        ...
    def test_tc_login_08_remember_me_not_checked(self):
        """
        Test Case TC_LOGIN_08:
        1. Navigate to login page.
        2. Enter valid registered email and password.
        3. Ensure 'Remember Me' is NOT checked.
        4. Click on the 'Login' button.
        5. Close and reopen the browser, revisit the site, and verify the user is logged out and redirected to the login page.
        """
        def driver_factory():
            return webdriver.Chrome()
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            page.tc_login_08_remember_me_not_checked(email="user1@example.com", password="ValidPassword123", driver_factory=driver_factory)
        finally:
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    unittest.main()
