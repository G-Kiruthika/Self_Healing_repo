import unittest
from selenium import webdriver
from Pages.SignUpPage import SignUpPage
from Pages.ProductSearchPage import ProductSearchPage
from Pages.CartPage import CartPage

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

class TestProductSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.product_search_page = ProductSearchPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_product_search_api(self):
        keyword = "laptop"
        # Send product search request via API
        response_json = self.product_search_page.send_product_search_request(keyword)
        # Validate the response
        self.assertTrue(self.product_search_page.validate_search_response(response_json, keyword), "API response validation failed for product search.")

    def test_product_search_ui(self):
        keyword = "laptop"
        # Perform product search via UI
        product_names = self.product_search_page.search_product_ui(keyword)
        self.assertTrue(len(product_names) > 0, "No products displayed in UI for keyword 'laptop'.")

class TestCartCreationUnauthorized(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://your-app-url/cart')
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_cart_creation_unauthenticated(self):
        """
        TC_CART_004: Attempt to create a shopping cart without authentication. System should deny request with unauthorized access error.
        """
        unauthorized_error_displayed = self.cart_page.attempt_create_cart()
        self.assertTrue(unauthorized_error_displayed, "Unauthorized access error should be displayed when attempting to create a cart without authentication.")

if __name__ == '__main__':
    unittest.main()
