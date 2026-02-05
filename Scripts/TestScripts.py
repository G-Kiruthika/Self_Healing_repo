# TestScripts.py
# Production-ready Selenium test script for TC_CART_001

import unittest
from selenium import webdriver
from SignUpPage import SignUpPage
from AuthPage import AuthPage
from CartApiPage import CartApiPage
from UserRegistrationAPIPage import UserRegistrationAPIPage
from ProductSearchPage import ProductSearchPage
from Pages.ProductPage import ProductPage
from Pages.CartPage import CartPage
from Pages.LoginPage import LoginPage
from Pages.HeaderPage import HeaderPage

class TestCartFunctionality(unittest.TestCase):
    def setUp(self):
        # Set up Selenium WebDriver (Chrome example, can be customized)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_TC_CART_001(self):
        pass # ... (existing code omitted for brevity)

    def test_TC_CART_005_add_product_exceed_stock(self):
        pass # ... (existing code omitted for brevity)

    def test_TC_CART_006_cart_persistence_after_sign_out_in(self):
        """
        Test Case: TC_CART_006
        Steps:
        1. Sign in as user and add products to cart. [Test Data: { "product_id": "111", "quantity": 2 }]
        2. Sign out and sign in again. [Test Data: { "username": "newuser1", "password": "StrongPass123" }]
        3. Query cart contents.
        Expected: Previously added products are present in cart after sign out/in.
        """
        # Step 1: Sign in as user
        login_page = LoginPage(self.driver)
        login_page.enter_username("newuser1")
        login_page.enter_password("StrongPass123")
        login_page.click_sign_in()

        # Step 2: Add product to cart
        product_page = ProductPage(self.driver)
        product_page.search_product("111")
        product_page.select_product("111")
        product_page.set_quantity(2)
        product_page.add_to_cart()

        # Step 3: Open cart and verify contents
        cart_page = CartPage(self.driver)
        cart_page.open_cart()
        cart_contents_before = cart_page.get_cart_contents()
        self.assertTrue(any(item["name"] == "111" and int(item["quantity"]) == 2 for item in cart_contents_before), "Product not present in cart before sign out.")

        # Step 4: Sign out
        header_page = HeaderPage(self.driver)
        header_page.click_sign_out()

        # Step 5: Sign in again
        header_page.click_sign_in_link()
        login_page.enter_username("newuser1")
        login_page.enter_password("StrongPass123")
        login_page.click_sign_in()

        # Step 6: Open cart and verify contents again
        cart_page.open_cart()
        cart_contents_after = cart_page.get_cart_contents()
        self.assertTrue(any(item["name"] == "111" and int(item["quantity"]) == 2 for item in cart_contents_after), "Product not present in cart after sign out/in.")

    def test_TC_CART_007_delete_cart_and_verify_absence(self):
        """
        Test Case: TC_CART_007
        Steps:
        1. Delete shopping cart for a user. [Test Data: { "cart_id": "<cart_id>" }]
        2. Query for deleted cart. [Test Data: { "cart_id": "<cart_id>" }]
        Expected:
        1. Cart and all associated products are deleted.
        2. Cart is not found.
        """
        cart_page = CartPage(self.driver)
        cart_page.open_cart()
        cart_page.delete_cart()
        self.assertTrue(cart_page.is_cart_deleted(), "Cart was not deleted or still found after deletion.")

if __name__ == "__main__":
    unittest.main()
