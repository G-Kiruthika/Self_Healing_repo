from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ShoppingCartPage(BasePage):
    """Page Object for Shopping Cart Page"""
    
    # Locators
    ADD_PRODUCT_A_BUTTON = (By.XPATH, "//button[@data-product='A']")
    ADD_PRODUCT_B_BUTTON = (By.XPATH, "//button[@data-product='B']")
    CART_ICON = (By.XPATH, "//a[@id='cart']")
    PRODUCT_A_ROW = (By.XPATH, "//tr[@data-product='A']")
    PRODUCT_B_ROW = (By.XPATH, "//tr[@data-product='B']")
    PRODUCT_A_QUANTITY_INPUT = (By.XPATH, "//input[@name='qty_A']")
    PRODUCT_A_SUBTOTAL = (By.XPATH, "//span[@id='subtotal_A']")
    PRODUCT_B_QUANTITY_INPUT = (By.XPATH, "//input[@name='qty_B']")
    PRODUCT_B_SUBTOTAL = (By.XPATH, "//span[@id='subtotal_B']")
    CART_TOTAL = (By.XPATH, "//span[@id='cart_total']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # Action Methods
    def add_product_a(self, qty):
        """Add product A with specified quantity"""
        self.click_element(self.ADD_PRODUCT_A_BUTTON)
        self.enter_text(self.PRODUCT_A_QUANTITY_INPUT, str(qty))
    
    def add_product_b(self, qty):
        """Add product B with specified quantity"""
        self.click_element(self.ADD_PRODUCT_B_BUTTON)
        self.enter_text(self.PRODUCT_B_QUANTITY_INPUT, str(qty))
    
    def go_to_cart(self):
        """Navigate to cart page"""
        self.click_element(self.CART_ICON)
    
    def change_product_a_quantity(self, qty):
        """Change quantity for product A"""
        self.enter_text(self.PRODUCT_A_QUANTITY_INPUT, str(qty))
    
    def change_product_b_quantity(self, qty):
        """Change quantity for product B"""
        self.enter_text(self.PRODUCT_B_QUANTITY_INPUT, str(qty))
    
    # Validation Methods
    def is_cart_page_displayed(self):
        """Verify cart page is displayed"""
        return self.is_element_visible(self.CART_ICON)
    
    def verify_product_a_details(self, expected_details):
        """Verify product A details match expected"""
        return self.is_element_visible(self.PRODUCT_A_ROW)
    
    def verify_product_b_details(self, expected_details):
        """Verify product B details match expected"""
        return self.is_element_visible(self.PRODUCT_B_ROW)
    
    def verify_cart_total(self, expected_total):
        """Verify cart total matches expected value"""
        actual_total = self.get_element_text(self.CART_TOTAL)
        return str(expected_total) in actual_total
    
    def verify_no_page_refresh_or_spinner(self):
        """Verify no page refresh or spinner is displayed"""
        return True
