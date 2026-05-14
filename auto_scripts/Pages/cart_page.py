from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Cart Page"""
    
    # Locators
    PRODUCT_A_ROW = (By.XPATH, "//tr[@data-product-name='Wireless Mouse']")
    PRODUCT_B_ROW = (By.XPATH, "//tr[@data-product-name='Coffee Subscription']")
    QUANTITY_INPUT_A = (By.XPATH, "//input[@name='quantity'][@data-product='Wireless Mouse']")
    QUANTITY_INPUT_B = (By.XPATH, "//input[@name='quantity'][@data-product='Coffee Subscription']")
    CART_TOTAL = (By.XPATH, "//span[@id='cart-total']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def add_product_to_cart(self, product_name, quantity):
        """Add product to cart with specified quantity"""
        pass
    
    def navigate_to_cart(self):
        """Navigate to cart page"""
        pass
    
    def change_product_quantity(self, product_name, quantity):
        """Change quantity of product in cart"""
        pass
    
    def verify_product_in_cart(self, product_name, quantity, subtotal):
        """Verify product is in cart with correct quantity and subtotal"""
        pass
    
    def verify_cart_total(self, expected_total):
        """Verify cart total matches expected value"""
        pass
    
    def verify_no_page_refresh_or_spinner(self):
        """Verify no page refresh or spinner after cart update"""
        pass
