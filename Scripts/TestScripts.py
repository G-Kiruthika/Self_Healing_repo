# imports
import unittest
from selenium import webdriver
from CartPage import CartPage
from pages.ProductSearchPage import ProductSearchPage
from PageClasses.CartAPIPage import CartAPIPage

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

    def test_cart_add_excess_quantity_tc_cart_005(self):
        """
        Test Case TC_CART_005:
        Attempt to add a product to cart with quantity greater than available stock.
        Test Data: { "product_id": "12345", "quantity": 101 }
        Acceptance Criteria: System returns error; product not added.
        """
        self.driver.get('https://example-ecommerce.com/product/12345')
        # Attempt to add product with excessive quantity
        try:
            quantity_input = self.driver.find_element_by_id('quantity')
            quantity_input.clear()
            quantity_input.send_keys('101')
            add_to_cart_button = self.driver.find_element_by_id('add-to-cart')
            add_to_cart_button.click()
            # Check for error message
            error_message = self.driver.find_element_by_id('cart-error').text
            self.assertIsNotNone(error_message, 'Error message should be displayed for excessive quantity.')
            self.assertIn('not added', error_message.lower(), 'Error message should mention product not added.')
        except Exception as e:
            self.fail(f'Exception occurred while testing excessive quantity add: {str(e)}')

    def test_cart_add_zero_quantity_tc_cart_010(self):
        """
        Test Case TC_CART_010:
        Attempt to add a product to cart with quantity zero.
        Test Data: { "product_id": "12345", "quantity": 0 }
        Acceptance Criteria: System returns error; product not added.
        """
        self.driver.get('https://example-ecommerce.com/product/12345')
        try:
            quantity_input = self.driver.find_element_by_id('quantity')
            quantity_input.clear()
            quantity_input.send_keys('0')
            add_to_cart_button = self.driver.find_element_by_id('add-to-cart')
            add_to_cart_button.click()
            error_message = self.driver.find_element_by_id('cart-error').text
            self.assertIsNotNone(error_message, 'Error message should be displayed for zero quantity.')
            self.assertIn('not added', error_message.lower(), 'Error message should mention product not added.')
        except Exception as e:
            self.fail(f'Exception occurred while testing zero quantity add: {str(e)}')

    def test_cart_access_denied_tc_cart_009(self):
        """
        Test Case TC_CART_009:
        Authenticate as User A and attempt to access User B's cart.
        Test Data: {"user_token": "userA", "cart_id": "cart_of_userB"}
        Acceptance Criteria: Access denied; error message returned.
        """
        self.driver.get('https://example-ecommerce.com')
        cart_api_page = CartAPIPage(self.driver)
        # Simulate User A attempting to access User B's cart
        user_token = 'userA'
        cart_id = 'cart_of_userB'
        response = cart_api_page.access_cart(user_token, cart_id)
        expected_message = 'You do not have permission to access this cart.'
        access_denied = cart_api_page.validate_access_denied_error(response, expected_message)
        self.assertTrue(access_denied, 'Access to another user's cart should be denied with the correct error message.')
        # Optional: print response for debug
        print('TC_CART_009 Response:', response)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()