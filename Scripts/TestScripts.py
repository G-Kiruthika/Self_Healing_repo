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
        response_json = self.product_search_page.send_product_search_request(keyword)
        self.assertTrue(self.product_search_page.validate_search_response(response_json, keyword), "API response validation failed for product search.")

    def test_product_search_ui(self):
        keyword = "laptop"
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

class TestCartExceedStock(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://your-app-url/cart')
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_add_product_exceed_stock_error(self):
        """
        TC_CART_005: Attempt to add a product to cart with quantity greater than available stock.
        System returns error; product not added.
        """
        product_id = '12345'
        quantity = 101
        add_result = self.cart_page.add_product_to_cart(product_id, quantity)
        error_message = self.cart_page.get_stock_error_message()
        self.assertIsNotNone(error_message, "Stock exceeded error message should be displayed when adding quantity greater than available stock.")
        self.assertIn('stock exceeded', error_message.lower(), "Error message should indicate stock exceeded.")

class TestCartDeleteAndVerify(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://your-app-url/cart')
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_delete_cart_and_verify_absence(self):
        """
        TC_CART_007: Delete shopping cart for a user, then query for deleted cart. Assert the cart and all associated products are deleted and the cart is not found.
        """
        cart_id = 'test_cart_007'
        # Step 1: Delete cart
        delete_result = self.cart_page.delete_cart(cart_id)
        self.assertTrue(delete_result, "Cart deletion action should be performed.")
        # Step 2: Query for deleted cart
        cart_present = self.cart_page.is_cart_present(cart_id)
        not_found_msg = self.cart_page.is_cart_not_found_message_displayed()
        self.assertFalse(cart_present, "Cart should not be present after deletion.")
        self.assertTrue(not_found_msg, "'Cart not found' message should be displayed after deletion.")

class TestCartAddInvalidProduct(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://your-app-url/cart')
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_add_product_with_invalid_id(self):
        """
        TC_CART_008: Attempt to add a product to cart with invalid product ID. System returns error; product not added.
        """
        product_id = '99999'
        quantity = 1
        error_displayed = self.cart_page.add_product_with_invalid_id(product_id, quantity)
        self.assertTrue(error_displayed, "Error message should be displayed when adding product with invalid ID.")

class TestCartAddZeroQuantity(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://your-app-url/cart')
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_add_product_with_zero_quantity(self):
        """
        TC_CART_010: Attempt to add a product to cart with quantity zero. System returns error; product not added.
        """
        product_id = '12345'
        error_displayed = self.cart_page.add_product_with_zero_quantity(product_id)
        self.assertTrue(error_displayed, "Error message should be displayed when adding product with zero quantity.")

class TestCartAccessDenied(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_access_cart_as_other_user_denied(self):
        """
        TC_CART_009: Authenticate as User A and attempt to access User B's cart. Access denied; error message returned.
        """
        user_id = 'userA'
        cart_id = 'cart_of_userB'
        self.cart_page.access_cart_as_user(user_id, cart_id)
        access_denied = self.cart_page.validate_access_denied()
        self.assertTrue(access_denied, "Access denied error message should be displayed when User A attempts to access User B's cart.")

if __name__ == '__main__':
    unittest.main()
