# TC_LOGIN_004_TestScript.py
"""
Selenium Automation Test Script for TC-LOGIN-004: Empty email field, valid password
This script validates the negative login scenario and ensures robust error reporting.
"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os

from auto_scripts.Pages.TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

class Test_TC_LOGIN_004(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up WebDriver (Chrome)
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        # Load locators
        locators_path = os.path.join("auto_scripts", "Locators", "Locators.json")
        cls.page = TC_LOGIN_004_TestPage(cls.driver, timeout=15, locators_path=locators_path)

    def test_tc_login_004(self):
        """
        1. Navigate to login page
        2. Leave email field empty
        3. Enter valid password
        4. Click Login button
        5. Validate error is displayed and login is prevented
        """
        valid_password = "ValidPass123!"
        url = "https://ecommerce.example.com/login"
        results = self.page.run_tc_login_004(valid_password, url)

        # Assert Step 1: Login page is displayed
        self.assertTrue(results["step_1_navigate_login"], f"Login page not displayed. Exception: {results['exception']}")
        # Assert Step 2: Email field remains blank
        self.assertTrue(results["step_2_leave_email_empty"], "Email field was not left blank.")
        # Assert Step 3: Password is entered
        self.assertTrue(results["step_3_enter_password"], "Password was not entered.")
        # Assert Step 4: Login button clicked
        self.assertTrue(results["step_4_click_login"], "Login button was not clicked.")
        # Assert Step 5: Validation error is displayed
        self.assertIsNotNone(results["step_5_validation_error"], "Validation error message not displayed.")
        self.assertTrue(
            "Email" in results["step_5_validation_error"] or "required" in results["step_5_validation_error"],
            f"Unexpected validation error: {results['step_5_validation_error']}"
        )
        # Assert Step 6: User remains on login page (login prevented)
        self.assertTrue(results["step_6_login_prevented"], "User is not on login page after failed login.")
        # Assert overall test pass
        self.assertTrue(results["overall_pass"], f"TC-LOGIN-004 failed. Exception: {results['exception']}" )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
