# Test Script for TC_SCRUM-74_001 using Selenium & LoginPage
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginTC_SCRUM_74_001(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.login_page = LoginPage(self.driver)

    def test_login_TC_SCRUM_74_001(self):
        """
        Test Case: TC_SCRUM-74_001
        Steps:
        1. Navigate to the login page
        2. Enter valid registered username
        3. Enter valid password
        4. Click on the Login button
        5. Verify user session is created and user profile is displayed
        """
        username = "testuser@example.com"
        password = "ValidPass123!"
        result = self.login_page.login_TC_SCRUM_74_001(username, password)
        self.assertTrue(result, "TC_SCRUM-74_001 failed: User was not logged in successfully!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
