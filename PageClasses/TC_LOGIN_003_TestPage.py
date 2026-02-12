import unittest
from selenium import webdriver
from PageClasses.LoginPage import LoginPage

class TC_LOGIN_003_TestPage(unittest.TestCase):
    """
    Test automation for TC_LOGIN_003: Forgot Username workflow
    Steps:
        1. Navigate to the login screen.
        2. Click on 'Forgot Username' link.
        3. Follow instructions to recover username.
    """
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.login_page = LoginPage(self.driver)

    def test_forgot_username_workflow(self):
        test_email = "user@example.com"
        # Step 1: Navigate to login screen
        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_on_login_page(), "Login screen is not displayed.")
        # Step 2: Click 'Forgot Username' link
        self.login_page.click_forgot_username()
        # Step 3: Recover username
        confirmation = self.login_page.start_forgot_username_workflow(test_email)
        self.assertIsNotNone(confirmation, "No confirmation or error message returned.")
        self.assertIn("username", confirmation.lower() or "success" in confirmation.lower(), "Username recovery did not succeed.")

    def tearDown(self):
        self.driver.quit()
