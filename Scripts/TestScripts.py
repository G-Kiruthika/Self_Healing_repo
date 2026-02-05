# imports
import unittest
from selenium import webdriver
from CartPage import CartPage
from pages.ProductSearchPage import ProductSearchPage

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

    def test_product_search_tc_cart_003(self):
        """
        Test Case TC_CART_003:
        Send a product search request with a valid keyword ('laptop').
        Acceptance Criteria: System returns matching products.
        """
        self.driver.get('https://example-ecommerce.com')
        search_page = ProductSearchPage(self.driver)
        results = search_page.search_and_validate_tc_cart_003(keyword='laptop')
        self.assertTrue(results.get('home_page_opened', False), 'Home page should open successfully.')
        self.assertTrue(results.get('search_performed', False), 'Search should be performed successfully.')
        self.assertTrue(results.get('has_results', False), 'At least one matching product should be returned.')
        self.assertTrue(results.get('all_names_match', False), 'All product names should contain the keyword "laptop".')
        self.assertTrue(results.get('pass', False), 'Search and validation should pass acceptance criteria.')
        # Optional: print results for debug
        print('TC_CART_003 Results:', results)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
