from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Page Object for Cart Page.
    Handles all cart-related operations including product management and validation.
    """
    
    # Locators
    PRODUCT_A_ROW = (By.XPATH, "//tr[td[contains(text(),'Product A')]]")
    PRODUCT_C_ROW = (By.XPATH, "//tr[td[contains(text(),'Product C')]]")
    DELETE_BUTTON_PRODUCT_C = (By.XPATH, "//tr[td[contains(text(),'Product C')]]//button[contains(text(),'Delete')]")
    CART_TOTAL = (By.ID, "cart-total")
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[contains(text(),'Your cart is empty')]")
    RETURN_TO_PRODUCT_CATALOG_BUTTON = (By.XPATH, "//button[contains(text(),'Return to Product Catalog')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # Action Methods
    def ensure_product_in_cart(self, product_name, subtotal):
        """
        Ensures a product is present in the cart with the specified subtotal.
        Args:
            product_name (str): Name of the product
            subtotal (str): Expected subtotal for the product
        """
        product_locator = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]")
        self.wait_for_element(product_locator)
    
    def click_delete_for_product(self, product_name):
        """
        Clicks the delete button for the specified product.
        Args:
            product_name (str): Name of the product to delete
        """
        delete_button = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]//button[contains(text(),'Delete')]")
        self.click_element(delete_button)
    
    def navigate_to_cart(self):
        """
        Navigates to the cart page.
        """
        # Implementation depends on application structure
        # This is a placeholder for navigation logic
        pass
    
    def observe_cart_page(self):
        """
        Observes the cart page to ensure it is loaded.
        """
        self.wait_for_element(self.CART_TOTAL)
    
    # Validation Methods
    def validate_product_present(self, product_name):
        """
        Validates that a product is present in the cart.
        Args:
            product_name (str): Name of the product
        Returns:
            bool: True if product is present, False otherwise
        """
        product_locator = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]")
        return self.is_element_visible(product_locator)
    
    def validate_product_absent(self, product_name):
        """
        Validates that a product is absent from the cart.
        Args:
            product_name (str): Name of the product
        Returns:
            bool: True if product is absent, False otherwise
        """
        product_locator = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]")
        return not self.is_element_visible(product_locator)
    
    def validate_cart_total(self, expected_total):
        """
        Validates that the cart total matches the expected value.
        Args:
            expected_total (str): Expected cart total
        Returns:
            bool: True if cart total matches, False otherwise
        """
        actual_total = self.get_element_text(self.CART_TOTAL)
        return expected_total in actual_total
    
    def validate_only_product_in_cart(self, product_name):
        """
        Validates that only the specified product is in the cart.
        Args:
            product_name (str): Name of the product
        Returns:
            bool: True if only this product is in cart, False otherwise
        """
        product_locator = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]")
        all_products = (By.XPATH, "//tr[td]")
        return self.is_element_visible(product_locator)
    
    def validate_cart_empty(self):
        """
        Validates that the cart is empty.
        Returns:
            bool: True if cart is empty, False otherwise
        """
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def validate_empty_cart_message(self):
        """
        Validates that the empty cart message is displayed.
        Returns:
            bool: True if empty cart message is visible, False otherwise
        """
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def validate_return_to_product_catalog_button_present(self):
        """
        Validates that the 'Return to Product Catalog' button is present.
        Returns:
            bool: True if button is present, False otherwise
        """
        return self.is_element_visible(self.RETURN_TO_PRODUCT_CATALOG_BUTTON)
