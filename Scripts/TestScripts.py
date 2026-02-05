# TestScripts.py
# Production-ready Selenium test script for TC_CART_001

import unittest
from selenium import webdriver
from SignUpPage import SignUpPage
from AuthPage import AuthPage
from CartApiPage import CartApiPage

class TestCartFunctionality(unittest.TestCase):
    def setUp(self):
        # Set up Selenium WebDriver (Chrome example, can be customized)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_TC_CART_001(self):
        """
        Test Case: TC_CART_001
        Steps:
        1. Sign up a new user (username: newuser1, email: newuser1@example.com, password: StrongPass123)
        2. Authenticate as this user
        3. Use the received token and user_id to create a cart via API
        """
        # Step 1: Sign up a new user
        signup_page = SignUpPage(self.driver)
        signup_result = signup_page.sign_up(
            username="newuser1",
            email="newuser1@example.com",
            password="StrongPass123"
        )
        self.assertTrue(signup_result['success'], f"Sign up failed: {signup_result.get('error', '')}")
        user_id = signup_result['user_id']

        # Step 2: Authenticate as this user
        auth_page = AuthPage(self.driver)
        auth_result = auth_page.authenticate(
            username="newuser1",
            password="StrongPass123"
        )
        self.assertTrue(auth_result['success'], f"Authentication failed: {auth_result.get('error', '')}")
        token = auth_result['token']

        # Step 3: Create a cart for the user via API
        cart_api_page = CartApiPage()
        cart_result = cart_api_page.create_cart(user_id=user_id, token=token)
        self.assertTrue(cart_result['success'], f"Cart creation failed: {cart_result.get('error', '')}")
        self.assertIn('cart_id', cart_result, "Cart ID not returned.")

if __name__ == "__main__":
    unittest.main()
