'''
Selenium Automation Test Script for TC-LOGIN-004

Test Scenario: Negative Login - Email Field Empty

This script uses the Page Object 'TC_LOGIN_004_TestPage' to automate and assert the negative login scenario where the email field is left empty and a valid password is entered.

Author: Automation Generator
'''

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import sys
import os
import time

# Ensure PageClass is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

class TestTCLOGIN004(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            raise RuntimeError(f"WebDriver initialization failed: {e}")
        cls.driver.implicitly_wait(3)
        cls.page = TC_LOGIN_004_TestPage(cls.driver)
        cls.valid_password = 'ValidPass123!'

    def test_tc_login_004(self):
        """
        Stepwise validation of TC-LOGIN-004: Empty email field, valid password.
        """
        # Run test flow
        results = self.page.run_tc_login_004(password=self.valid_password)

        # Step 1: Should navigate to login page
        self.assertTrue(results['step_1_navigate_login'], msg='Login page should be displayed.')

        # Step 2: Email field left empty (no assertion needed, but step should be True)
        self.assertTrue(results['step_2_leave_email_empty'], msg='Email field should be left empty.')

        # Step 3: Password entered
        self.assertTrue(results['step_3_enter_password'], msg='Password should be entered and masked.')

        # Step 4: Click Login button
        self.assertTrue(results['step_4_click_login'], msg='Login button should be clicked.')

        # Step 5: Validation error should be displayed
        self.assertIsNotNone(results['step_5_validation_error'], msg='Validation error message must be shown.')
        self.assertTrue(
            'email' in results['step_5_validation_error'].lower() or 'required' in results['step_5_validation_error'].lower(),
            msg=f"Unexpected validation error message: {results['step_5_validation_error']}"
        )

        # Step 6: User must remain on login page (login prevented)
        self.assertTrue(results['step_6_login_prevented'], msg='User should remain on login page after failed login.')

        # Overall pass
        self.assertTrue(results['overall_pass'], msg='Test should overall pass if all validations succeeded.')

        # No unexpected exception
        self.assertIsNone(results['exception'], msg=f"Unexpected exception occurred: {results['exception']}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
