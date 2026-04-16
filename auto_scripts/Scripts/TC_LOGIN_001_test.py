import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.TC_LOGIN_001_TestPage import TC_LOGIN_001_TestPage

class Test_TC_LOGIN_001(unittest.TestCase):
    """
    Selenium Automation Script for Test Case TC_LOGIN_001
    Valid Login: End-to-end authentication and session validation.
    """
    EMAIL = "testuser@example.com"
    PASSWORD = "ValidPass123!"
    LOGIN_URL = "https://app.example.com/login"

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.test_page = TC_LOGIN_001_TestPage(cls.driver, timeout=10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_tc_login_001(self):
        """
        Steps:
        1. Navigate to login page
        2. Enter valid email
        3. Enter valid password
        4. Click Login
        5. Assert dashboard and profile displayed
        6. Assert session token created
        """
        results = self.test_page.run_tc_login_001(self.EMAIL, self.PASSWORD)
        # Step 1: Navigate to login page
        self.assertTrue(results["step_1_navigate_login"], "Login page should be displayed with email and password fields.")
        # Step 2: Enter valid email
        self.assertTrue(results["step_2_enter_email"], "Email should be accepted and displayed in the field.")
        # Step 3: Enter valid password
        self.assertTrue(results["step_3_enter_password"], "Password should be masked and accepted.")
        # Step 4: Click Login
        self.assertTrue(results["step_4_click_login"], "Login button should be clickable.")
        # Step 5: Assert dashboard displayed
        self.assertTrue(results["step_5_dashboard_displayed"], "User should be redirected to the dashboard after login.")
        # Step 6: Assert profile displayed
        self.assertTrue(results["step_6_profile_displayed"], "User profile should be displayed after login.")
        # Step 7: Assert session token created
        self.assertTrue(results["step_7_session_token_created"], "User session token should be generated.")
        # Overall test pass
        self.assertTrue(results["overall_pass"], f"End-to-end login workflow failed. Exception: {results['exception']}")

if __name__ == "__main__":
    unittest.main()
