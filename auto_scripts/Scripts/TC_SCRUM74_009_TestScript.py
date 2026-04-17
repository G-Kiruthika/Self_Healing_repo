# TC_SCRUM74_009_TestScript.py
"""
Automated Selenium test script for TC_SCRUM74_009: Username Recovery Workflow.
- Validates end-to-end username recovery flow as described in test case.
- Uses PageClasses: LoginPage, UsernameRecoveryPage, TC_SCRUM74_009_TestPage.
"""

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_SCRUM74_009_TestPage import TC_SCRUM74_009_TestPage

class Test_TC_SCRUM74_009(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_username_recovery_workflow(self):
        """
        End-to-end test for username recovery workflow (TC_SCRUM74_009).
        Steps:
        1. Navigate to login page
        2. Validate presence of Forgot Username link
        3. Click Forgot Username link
        4. Verify redirection to username recovery page
        5. Validate presence of email/phone input and submit button
        """
        tc_page = TC_SCRUM74_009_TestPage(self.driver, timeout=10)
        results = tc_page.run_tc_scrum74_009()

        # Step 1: Login page displayed
        self.assertTrue(results["step_1_navigate_login"], "Login page not displayed.")

        # Step 2: Forgot Username link present
        self.assertTrue(results["step_2_forgot_username_link_present"], "Forgot Username link not found.")

        # Step 3: Click action successful
        self.assertTrue(results["step_3_click_forgot_username"], "Failed to click Forgot Username link.")

        # Step 4: Username recovery page loaded
        self.assertTrue(results["step_4_on_username_recovery_page"], "Username recovery page not loaded.")

        # Step 5: Recovery page elements validation
        element_results = results["step_5_validate_recovery_elements"]
        self.assertIsNotNone(element_results, "Element validation failed.")
        self.assertTrue(element_results["email_or_phone_present"], "Email/Phone input field not present.")
        self.assertTrue(element_results["submit_button_present"], "Submit button not present.")
        self.assertTrue(results["overall_pass"], "Overall test failed.")
        self.assertIsNone(results["exception"], f"Exception occurred: {results['exception']}")

if __name__ == "__main__":
    unittest.main()
