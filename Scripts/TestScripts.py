import unittest
from selenium import webdriver
from Pages.SignUpPage import SignUpPage

class TestSignUpDuplicateEmail(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://your-app-url/sign-up')
        self.signup_page = SignUpPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_duplicate_email_error(self):
        self.signup_page.enter_username('user2')
        self.signup_page.enter_email('newuser1@example.com')
        self.signup_page.enter_password('AnotherPass123')
        self.signup_page.click_signup()
        self.assertTrue(self.signup_page.is_duplicate_email_error_displayed(), 'Duplicate email error message should be displayed.')

if __name__ == '__main__':
    unittest.main()
