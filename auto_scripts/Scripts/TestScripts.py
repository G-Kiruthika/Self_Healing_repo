import unittest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...

    def test_tc_login_017_verify_password_field_masking(self):
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.tc_login_017_verify_password_field_masking('ValidPass123')
            self.assertTrue(result, "TC_LOGIN_017 failed: Password field masking not verified.")
        finally:
            driver.quit()

    def test_tc010_login_attempts_with_lockout(self):
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.login_attempts_with_lockout_tc010()
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

    def test_tc_login_01_valid_login(self):
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            page.go_to_login_page()
            page.enter_email('user1@example.com')
            page.enter_password('ValidPassword123')
            page.click_login()
            self.assertTrue(page.is_dashboard_displayed(), "TC_LOGIN_01 failed: Dashboard not displayed after valid login.")
        finally:
            driver.quit()

    def test_tc012_xss_email_field(self):
        """
        Test Case TC012:
        1. Enter XSS payload in email field. [Test Data: <script>alert('xss')</script>]
        2. Verify application does not execute script; error message or input sanitized.
        Acceptance Criteria: 8
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.test_xss_email_field()
            self.assertTrue(result, "TC012 failed: XSS input in email field was not handled properly.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
