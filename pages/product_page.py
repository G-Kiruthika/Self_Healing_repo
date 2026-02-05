# product_page.py
"""
ProductPage class for adding products to the cart.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    def add_product_to_cart(self, product_id, quantity):
        """
        Adds a product to the cart by product_id and quantity.
        """
        # Locators are placeholders and should be updated as per actual application
        PRODUCT_INPUT = (By.ID, f'product_{product_id}_qty')
        ADD_TO_CART_BUTTON = (By.ID, f'add_to_cart_{product_id}')
        self.enter_text(*PRODUCT_INPUT, text=str(quantity))
        self.click(*ADD_TO_CART_BUTTON)
