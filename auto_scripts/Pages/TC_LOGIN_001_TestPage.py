import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from PageClasses.LoginPage import LoginPage

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
        # You may use Chrome, Firefox, etc. depending on your setup
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
        try:
            self.login_page.perform_invalid_login_and_validate(invalid_email, invalid_password)
        except AssertionError as ae:
            self.fail(f"Test failed: {ae}")
        except Exception as e:
            self.fail(f"Unexpected error during test execution: {e}")

if __name__ == "__main__":
    unittest.main()