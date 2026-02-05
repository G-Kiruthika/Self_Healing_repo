# Existing content of TestScripts.py
# ... (existing test methods)

import unittest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...

    def test_tc_login_017_verify_password_field_masking(self):
        """
        Test Case TC_LOGIN_017:
        1. Navigate to login page and verify display.
        2. Enter password 'ValidPass123' and verify masking.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.tc_login_017_verify_password_field_masking('ValidPass123')
            self.assertTrue(result, "TC_LOGIN_017 failed: Password field masking not verified.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
