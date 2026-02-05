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

    def test_tc_login_01_valid_login(self):
        """
        Test Case TC_LOGIN_01:
        1. Navigate to the login page.
        2. Enter a valid registered email address ('user1@example.com').
        3. Enter a valid password ('ValidPassword123').
        4. Click on the 'Login' button.
        5. Assert user is successfully logged in and redirected to the dashboard.
        """
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

    def test_tc_login_02_invalid_password(self):
        """
        Test Case TC_LOGIN_02:
        1. Navigate to the login page.
        2. Enter a valid registered email address ('user1@example.com').
        3. Enter an invalid password ('WrongPass!@#').
        4. Click on the 'Login' button.
        5. Assert error message 'Invalid email or password' is displayed and user remains on the login page.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            page.go_to_login_page()
            page.enter_email('user1@example.com')
            page.enter_password('WrongPass!@#')
            page.click_login()
            error_msg = page.get_error_message()
            self.assertEqual(error_msg, 'Invalid email or password', f"TC_LOGIN_02 failed: Expected error 'Invalid email or password', got '{error_msg}'")
            self.assertTrue(page.is_on_login_page(), "TC_LOGIN_02 failed: User is not on the login page after failed login.")
        finally:
            driver.quit()

    def test_tc013_concurrent_login_load(self):
        """
        Test Case TC013:
        Simulate 1000 concurrent login attempts with valid credentials and verify system resilience.
        Acceptance Criteria:
        - System responds within acceptable time; no errors or crashes.
        """
        # Prepare 1000 valid credentials
        credentials = [
            {"email": f"user{i}@example.com", "password": "Password123!"} for i in range(1, 1001)
        ]
        # Run concurrent login simulation
        page = LoginPage(None)  # Not used in threaded method, so can be None
        results = page.simulate_concurrent_logins(credentials, max_threads=1000)
        # Assert no system errors or crashes
        failure_count = 0
        for r in results:
            if r["status"] != "SUCCESS":
                # Accept handled errors, but count system-level failures
                if "WebDriver error" in r["message"] or "Exception" in r["message"]:
                    failure_count += 1
        # Log summary
        print(f"TC013: Total successful logins: {sum(1 for r in results if r['status']=='SUCCESS')} / {len(results)}")
        print(f"TC013: System-level failures: {failure_count}")
        # The test passes if there are no system-level failures
        self.assertEqual(failure_count, 0, f"TC013 failed: {failure_count} system-level errors/crashes occurred during concurrent logins.")

    def test_tc_login_03_invalid_login(self):
        """
        Test Case TC_LOGIN_03:
        1. Navigate to the login page.
        2. Enter an unregistered email address ('nouser@example.com').
        3. Enter any password ('AnyPassword1!').
        4. Click on the 'Login' button.
        5. Assert error message 'Invalid email or password' is displayed and user remains on the login page.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.tc_login_03_invalid_login('nouser@example.com', 'AnyPassword1!')
            self.assertTrue(result, "TC_LOGIN_03 failed: Error message not displayed or user not on login page.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
