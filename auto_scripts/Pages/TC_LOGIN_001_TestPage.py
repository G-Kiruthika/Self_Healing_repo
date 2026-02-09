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
    @classmethod
    def setUpClass(cls):
        """
        Setup test resources. Uses Chrome WebDriver; update as needed for your environment.
        """
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up test resources.
        """
        try:
            cls.driver.quit()
        except WebDriverException:
            pass

    def test_invalid_login(self):
        """
        TC_LOGIN_001: Attempt login with invalid credentials and verify error message and page state.
        """
        invalid_email = "invalid@example.com"
        invalid_password = "wrongpassword"
        try:
            self.login_page.perform_invalid_login_and_validate(invalid_email, invalid_password)
        except AssertionError as ae:
            self.fail(f"Test failed: {ae}")
        except Exception as e:
            self.fail(f"Unexpected error during test execution: {e}")

    def test_invalid_login_empty_fields(self):
        """
        Additional negative test: Attempt login with empty fields and verify error handling.
        """
        try:
            self.login_page.login_with_credentials("", "")
            error_msg = self.login_page.get_error_message()
            self.assertIsNotNone(error_msg, "Error message not found for empty fields.")
            self.assertTrue("Mandatory fields" in error_msg or "Invalid username or password" in error_msg,
                            f"Unexpected error message: {error_msg}")
            self.assertTrue(self.login_page.is_on_login_page(), "User is not on login page after empty login.")
        except AssertionError as ae:
            self.fail(f"Test failed: {ae}")
        except Exception as e:
            self.fail(f"Unexpected error during empty field test: {e}")

if __name__ == "__main__":
    unittest.main()
