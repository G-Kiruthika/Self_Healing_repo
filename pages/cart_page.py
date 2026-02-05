# cart_page.py
"""
CartPage class for querying cart contents.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = (By.CSS_SELECTOR, '.cart-item')
    PRODUCT_ID = (By.CSS_SELECTOR, '.product-id')
    QUANTITY = (By.CSS_SELECTOR, '.quantity')

    def get_cart_contents(self):
        """
        Returns a list of dicts with product_id and quantity for all items in the cart.
        """
        items = self.driver.find_elements(*self.CART_ITEMS)
        cart_contents = []
        for item in items:
            product_id = item.find_element(*self.PRODUCT_ID).text
            quantity = int(item.find_element(*self.QUANTITY).text)
            cart_contents.append({'product_id': product_id, 'quantity': quantity})
        return cart_contents
