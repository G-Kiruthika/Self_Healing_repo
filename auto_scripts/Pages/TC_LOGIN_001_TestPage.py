import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage

class TC_LOGIN_001_TestPage(unittest.TestCase):
    """
    Test Page for TC_LOGIN_001 - Invalid Login Scenario
    Steps:
        1. Navigate to the login screen.
        2. Enter invalid username and/or password.
        3. Click Login button.
        4. Validate error message 'Invalid username or password. Please try again.' is displayed.
        5. Assert user remains on login page after failed login.
    """
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        try:
            self.driver.quit()
        except WebDriverException:
            pass

    def test_invalid_login(self):
        invalid_email = "invalid@example.com"
        invalid_password = "wrongpassword"
        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_on_login_page(), "Login page not displayed.")
        # Step 2 & 3: Enter invalid credentials and click login
        self.login_page.enter_email(invalid_email)
        self.login_page.enter_password(invalid_password)
        self.login_page.click_login()
        # Step 4: Validate error message
        error_msg = self.login_page.get_error_message()
        self.assertIsNotNone(error_msg, "Error message not found after invalid login.")
        self.assertEqual(error_msg.strip(), "Invalid username or password. Please try again.", f"Expected error message not found. Got: {error_msg.strip()}")
        # Step 5: Assert user remains on login page
        self.assertTrue(self.login_page.is_on_login_page(), "User did not remain on login page after failed login.")

if __name__ == "__main__":
    unittest.main()