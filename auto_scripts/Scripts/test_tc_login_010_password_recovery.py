# test_tc_login_010_password_recovery.py
"""
Automated Selenium Test for TC_LOGIN_010: Password Recovery Workflow
Covers navigation, email entry, submission, success validation, and inbox check.
Author: Automation
"""
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import sys
import os

# Ensure Pages module is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from PasswordRecoveryPage import PasswordRecoveryPage

class TestPasswordRecoveryTCLogin010(unittest.TestCase):
    EMAIL = "testuser@example.com"
    EXPECTED_SUCCESS_MSG = "Password reset link has been sent to your email"
    RECOVERY_URL = "https://app.example.com/forgot-password"

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)
        cls.page = PasswordRecoveryPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_tc_login_010_password_recovery(self):
        """
        Test Steps:
        1. Navigate to the password recovery page via Forgot Password link
        2. Enter registered email address
        3. Click on the Submit button
        4. Validate success message
        5. Check email inbox for password reset link (mocked)
        """
        results = self.page.run_tc_login_010(self.EMAIL)

        # Step 1: Navigate to password recovery page
        self.assertTrue(results["step_1_navigate_recovery"], "Step 1 failed: Could not navigate to password recovery page.")
        self.assertEqual(self.page.driver.current_url, self.RECOVERY_URL, "Step 1 failed: Not on expected recovery URL.")

        # Step 2: Enter registered email address
        self.assertTrue(results["step_2_enter_email"], "Step 2 failed: Could not enter email.")

        # Step 3: Click Submit button
        self.assertTrue(results["step_3_click_submit"], "Step 3 failed: Could not click submit.")

        # Step 4: Validate success message
        self.assertIsNotNone(results["step_4_success_message"], "Step 4 failed: Success message not found.")
        self.assertIn(self.EXPECTED_SUCCESS_MSG, results["step_4_success_message"], f"Step 4 failed: Success message incorrect. Actual: {results['step_4_success_message']}")

        # Step 5: Check email inbox for password reset link (mocked)
        self.assertIsNotNone(results["step_5_email_inbox_check"], "Step 5 failed: Reset link not found in email inbox.")
        self.assertRegex(results["step_5_email_inbox_check"], r"https://app\.example\.com/reset-password\?token=.+&expires=\d+", "Step 5 failed: Reset link format invalid.")

        # Overall pass
        self.assertTrue(results["overall_pass"], f"Test failed overall. Exception: {results['exception']}")

if __name__ == "__main__":
    unittest.main()
