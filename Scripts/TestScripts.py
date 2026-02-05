# TestScripts.py
# Automated test for TC_CART_009: Access Denied to Another User's Cart

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from Pages.CartPage import CartPage

class TestCartAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def mock_login_function(self, credentials):
        self.driver.get('https://your-app-url/login')
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.ID, 'login_button')
        username_field.clear()
        username_field.send_keys(credentials['username'])
        password_field.clear()
        password_field.send_keys(credentials['password'])
        login_button.click()

    def test_TC_CART_009_access_denied_to_other_users_cart(self):
        userA_credentials = {'username': 'userA', 'password': 'passwordA'}
        cart_of_userB_id = 'cart_of_userB'
        error_message_locator = (By.ID, 'cart_error_message')
        expected_error_text = 'Access Denied: You do not have permission to view this cart.'
        result = self.cart_page.verify_access_denied_for_other_user_cart(
            userA_credentials=userA_credentials,
            cart_of_userB_id=cart_of_userB_id,
            error_message_locator=error_message_locator,
            expected_error_text=expected_error_text,
            login_function=self.mock_login_function
        )
        self.assertTrue(result, 'Access denial verification failed for TC_CART_009.')

    def test_TC_CART_010_add_product_with_quantity_zero_expect_error(self):
        """
        TC_CART_010: Add product to cart with quantity zero, expect error.
        """
        self.driver.get('https://your-app-url/cart')
        expected_error_message = "Quantity must be greater than zero."
        error_message = self.cart_page.add_product_with_quantity(0)
        self.assertIsNotNone(error_message, "No error message returned when adding product with quantity zero.")
        self.assertEqual(error_message, expected_error_message, f"Expected error message '{expected_error_message}', but got '{error_message}'.")

    def test_TC_CART_004_attempt_cart_creation_without_authentication(self):
        """
        TC_CART_004: Attempt to create a shopping cart without authentication.
        Acceptance Criteria: System denies request; error for unauthorized access.
        """
        self.driver.get('https://your-app-url/cart')
        result = self.cart_page.attempt_cart_creation_without_authentication()
        self.assertTrue(result, "Unauthorized access error was not displayed when attempting cart creation without authentication.")

if __name__ == '__main__':
    unittest.main()
