"""
Selenium Automation Test Script for TC_LOGIN_001
Author: Automation Generator
Description: Automated test for valid login scenario using TC_LOGIN_001_TestPage PageClass.
This script can be executed directly or integrated into CI/CD pipelines.
"""

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_001_TestPage import TC_LOGIN_001_TestPage
import time

class TestTCLogin001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_valid_login(self):
        """
        Test Case: TC_LOGIN_001
        Steps:
        1. Navigate to login page
        2. Enter valid email and password
        3. Click Login button
        4. Validate authentication and dashboard/profile display
        5. Validate session token creation
        """
        email = "testuser@example.com"
        password = "ValidPass123!"
        test_page = TC_LOGIN_001_TestPage(self.driver)
        results = test_page.run_tc_login_001(email, password)

        # Stepwise assertions
        self.assertTrue(results["step_1_navigate_login"], "Login page was not displayed.")
        self.assertTrue(results["step_2_enter_email"], "Email was not entered correctly.")
        self.assertTrue(results["step_3_enter_password"], "Password was not entered correctly.")
        self.assertTrue(results["step_4_click_login"], "Login button click failed.")
        self.assertTrue(results["step_5_dashboard_displayed"], "Dashboard was not displayed after login.")
        self.assertTrue(results["step_6_profile_displayed"], "User profile was not displayed after login.")
        self.assertTrue(results["step_7_session_token_created"], "Session token was not generated.")
        self.assertTrue(results["overall_pass"], f"Test failed: {results.get('exception', '')}")

if __name__ == "__main__":
    unittest.main()
