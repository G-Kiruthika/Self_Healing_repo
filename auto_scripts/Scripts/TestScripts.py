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

    def test_tc010_login_attempts_with_lockout(self):
        """
        Test Case TC010:
        1. Attempt login with invalid password 5 times.
        2. Attempt login with correct credentials after lockout.
        3. Assert error messages and lockout behavior as per the test case and PageClass implementation.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            # Call the PageClass method for TC010
            result = page.login_attempts_with_lockout_tc010()
            # Validate returned results
            self.assertIsInstance(result, dict, "TC010 failed: Result should be a dictionary.")
            self.assertIn("invalid_attempts", result, "TC010 failed: Missing invalid_attempts key.")
            self.assertEqual(result["invalid_attempts"], 5, "TC010 failed: Should have 5 invalid attempts.")
            self.assertIn("lockout_triggered", result, "TC010 failed: Missing lockout_triggered key.")
            self.assertTrue(result["lockout_triggered"], "TC010 failed: Lockout was not triggered after 5 invalid attempts.")
            self.assertIn("lockout_message", result, "TC010 failed: Missing lockout_message key.")
            self.assertTrue("locked out" in result["lockout_message"].lower(), "TC010 failed: Lockout message not shown.")
            self.assertIn("valid_login_after_lockout", result, "TC010 failed: Missing valid_login_after_lockout key.")
            self.assertFalse(result["valid_login_after_lockout"], "TC010 failed: Valid login should not succeed during lockout.")
            self.assertIn("valid_login_message", result, "TC010 failed: Missing valid_login_message key.")
            self.assertTrue("locked out" in result["valid_login_message"].lower(), "TC010 failed: Lockout message should appear when trying correct credentials after lockout.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
