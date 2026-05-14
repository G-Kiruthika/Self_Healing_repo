from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Cart Page"""
    
    # Locators
    PRODUCT_A_ROW = (By.XPATH, "//div[@data-product='A']")
    PRODUCT_C_ROW = (By.XPATH, "//div[@data-product='C']")
    DELETE_BUTTON_C = (By.XPATH, "//button[@data-action='delete'][@data-product='C']")
    CART_TOTAL = (By.XPATH, "//span[@id='cart-total']")
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(), 'Your cart is empty')]")
    RETURN_TO_CATALOG_BUTTON = (By.XPATH, "//button[contains(text(), 'Return to Product Catalog')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def ensure_product_in_cart(self, product_name, subtotal):
        """Ensure product is in cart with specified subtotal"""
        if product_name == 'A':
            product_row = self.find_element(self.PRODUCT_A_ROW)
        elif product_name == 'C':
            product_row = self.find_element(self.PRODUCT_C_ROW)
        else:
            raise ValueError(f"Unknown product: {product_name}")
        return self.is_element_visible((By.XPATH, f"//div[@data-product='{product_name}']//span[contains(text(), '{subtotal}')]"))
    
    def click_delete_for_product(self, product_name):
        """Click delete button for specified product"""
        if product_name == 'C':
            self.click_element(self.DELETE_BUTTON_C)
        else:
            self.click_element((By.XPATH, f"//button[@data-action='delete'][@data-product='{product_name}']"))
    
    def navigate_to_cart_page(self):
        """Navigate to cart page"""
        self.driver.get("https://example-ecommerce.com/cart")
    
    def observe_cart_page(self):
        """Observe cart page state"""
        return self.is_element_visible(self.CART_TOTAL) or self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def verify_product_present(self, product_name):
        """Verify product is present in cart"""
        if product_name == 'A':
            return self.is_element_visible(self.PRODUCT_A_ROW)
        elif product_name == 'C':
            return self.is_element_visible(self.PRODUCT_C_ROW)
        else:
            return self.is_element_visible((By.XPATH, f"//div[@data-product='{product_name}']"))
    
    def verify_product_not_present(self, product_name):
        """Verify product is not present in cart"""
        return not self.verify_product_present(product_name)
    
    def verify_cart_total(self, expected_total):
        """Verify cart total matches expected value"""
        cart_total_element = self.find_element(self.CART_TOTAL)
        actual_total = cart_total_element.text.strip()
        return actual_total == expected_total
    
    def verify_empty_cart_message_displayed(self):
        """Verify empty cart message is displayed"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def verify_no_product_line_items(self):
        """Verify no product line items are present in cart"""
        return not self.is_element_visible(self.PRODUCT_A_ROW) and not self.is_element_visible(self.PRODUCT_C_ROW)
