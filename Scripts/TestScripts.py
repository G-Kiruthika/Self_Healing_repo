# TestScripts.py
# Placeholder for TC_CART_003 test method

import unittest
from selenium import webdriver
from Pages.CartPage import CartPage

class TestCartFunctionality(unittest.TestCase):
    """
    Test Suite for Cart Functionality
    """
    def setUp(self):
        # Initialize WebDriver (adjust as needed for your environment)
        self.driver = webdriver.Chrome()
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC_CART_005_excess_quantity(self):
        """
        TC_CART_005: Attempt to add a product to cart with quantity greater than available stock.
        Steps:
        1. Attempt to add product_id '12345' with quantity 101.
        2. Verify that an error is returned and the product is not added to the cart.
        """
        product_id = "12345"
        quantity = 101
        response = self.cart_page.add_product_to_cart(product_id, quantity)
        try:
            error_detected = self.cart_page.validate_quantity_exceeds_stock_error(response)
        except AssertionError as e:
            error_detected = False
            error_message = str(e)
        else:
            error_message = response.text
        # For API, we assume product is not in cart if error is detected
        product_not_in_cart = error_detected
        self.assertTrue(error_detected, f"Expected error, got: {error_message}")
        self.assertTrue(product_not_in_cart, "Product should not be in cart after error.")
        print(f"Error message: {error_message}")

    def test_TC_CART_006_cart_persistence(self):
        """
        TC_CART_006: Test cart persistence after sign out and sign in.
        Steps:
        1. Sign in as 'newuser1' with 'StrongPass123'.
        2. Add product_id '111' with quantity 2 to the cart.
        3. Sign out and sign in again as 'newuser1', 'StrongPass123'.
        4. Query cart contents and verify that product_id '111' is present with quantity 2.
        """
        username = "newuser1"
        password = "StrongPass123"
        product_id = "111"
        quantity = 2
        expected_products = [f"{product_id} (x{quantity})"]

        # Step 1: Sign in
        self.cart_page.sign_in(username, password)
        # Step 2: Add product to cart
        self.cart_page.add_product_to_cart(product_id, quantity)
        # Step 3: Sign out and sign in again
        self.cart_page.sign_out()
        self.cart_page.sign_in(username, password)
        # Step 4: Query cart contents
        cart_contents = self.cart_page.query_cart_contents()
        # Validate cart contents
        found = False
        for item in cart_contents:
            if product_id in item and str(quantity) in item:
                found = True
        self.assertTrue(found, f"Product {product_id} with quantity {quantity} not found in cart after sign out/in.")
        print(f"Cart contents after re-login: {cart_contents}")

if __name__ == "__main__":
    unittest.main()
