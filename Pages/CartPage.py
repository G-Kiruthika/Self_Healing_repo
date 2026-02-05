import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class CartPage:
    CART_API_URL = 'https://example-ecommerce.com/api/cart'
    CART_BUTTON = (By.CSS_SELECTOR, '#cart-btn')
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '.add-to-cart')
    CART_ITEM_LIST = (By.CSS_SELECTOR, '#cart-items')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open_cart(self):
        cart_btn = self.driver.find_element(*self.CART_BUTTON)
        cart_btn.click()

    def add_product_to_cart(self, product_id: str, quantity: int):
        """
        Attempts to add a product to cart using the API (simulating backend behavior).
        Returns response dict.
        """
        payload = {
            "product_id": product_id,
            "quantity": quantity
        }
        response = requests.post(self.CART_API_URL, json=payload)
        return response.json()

    def validate_add_zero_quantity(self, product_id: str):
        """
        Attempts to add a product with quantity zero and validates error response and absence in cart.
        """
        api_response = self.add_product_to_cart(product_id, 0)
        assert 'error' in api_response, f"Expected error in API response, got: {api_response}"
        self.open_cart()
        cart_items = self.driver.find_elements(*self.CART_ITEM_LIST)
        product_in_cart = any(product_id in item.text for item in cart_items)
        assert not product_in_cart, f"Product {product_id} should not be in cart when quantity is zero."