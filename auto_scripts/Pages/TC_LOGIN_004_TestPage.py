import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage

class TC_LOGIN_004_TestPage(unittest.TestCase):
    """
    Test Page for TC_LOGIN_004
    Test Case ID: 4165
    Description: Leave username empty, enter valid password, click login, validate error message.
    Strict adherence to Selenium Python automation standards.
    """
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        try:
            self.driver.quit()
        except WebDriverException:
            pass

    def test_tc_login_004(self):
        """
        Steps:
            1. Navigate to Login Page.
            2. Leave username field empty.
            3. Enter valid password.
            4. Click Login button.
            5. Validate error message 'Username is required' is displayed.
        """
        results = self.login_page.run_tc_login_004('ValidPass123!')
        self.assertTrue(results['pass'], f"TC_LOGIN_004 failed: {results}")

if __name__ == "__main__":
    unittest.main()
