# imports
import unittest
from selenium import webdriver
from CartPage import CartPage

class TestCartDuplicateSignup(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://example-ecommerce.com')
        self.cart_page = CartPage(self.driver)

    def test_duplicate_email_signup(self):
        username = 'user2'
        email = 'newuser1@example.com'
        password = 'AnotherPass123'
        error_message = self.cart_page.attempt_duplicate_signup(username, email, password)
        self.assertIsNotNone(error_message, 'Error message should be displayed for duplicate email signup.')
        self.assertIn('duplicate', error_message.lower(), 'Error message should mention duplicate email.')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
