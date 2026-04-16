"""
Test Script: test_TC_LOGIN_001.py

Automates: TC_LOGIN_001 - Valid Login Workflow

- Navigates to login page
- Enters valid credentials
- Clicks login
- Asserts dashboard and profile
- Validates session token

Author: Automation Generator
"""

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.TC_LOGIN_001_TestPage import TC_LOGIN_001_TestPage
import time

class Test_TC_LOGIN_001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            raise Exception(f"WebDriver initialization failed: {e}")
        cls.driver.implicitly_wait(5)
        cls.page = TC_LOGIN_001_TestPage(cls.driver, timeout=10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_tc_login_001_valid_login(self):
        """
        Test Case TC_LOGIN_001: Valid Login Workflow
        Steps:
            1. Navigate to login page
            2. Enter valid email
            3. Enter valid password
            4. Click Login
            5. Validate dashboard
            6. Validate profile display
            7. Validate session token
        """
        # Test Data
        email = "testuser@example.com"
        password = "ValidPass123!"
        results = self.page.run_tc_login_001(email, password)

        # Step 1: Login page displayed
        self.assertTrue(results["step_1_navigate_login"], "Login page was not displayed as expected.")
        # Step 2: Email entry
        self.assertTrue(results["step_2_enter_email"], "Email was not entered/accepted.")
        # Step 3: Password entry
        self.assertTrue(results["step_3_enter_password"], "Password was not entered/accepted.")
        # Step 4: Click Login
        self.assertTrue(results["step_4_click_login"], "Login button click failed.")
        # Step 5: Dashboard displayed
        self.assertTrue(results["step_5_dashboard_displayed"], "Dashboard was not displayed after login.")
        # Step 6: Profile icon displayed
        self.assertTrue(results["step_6_profile_displayed"], "Profile icon was not displayed after login.")
        # Step 7: Session token created
        self.assertTrue(results["step_7_session_token_created"], "Session token was not created/validated.")
        # Overall pass
        self.assertTrue(results["overall_pass"], f"Overall login workflow failed. Exception: {results['exception']}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
