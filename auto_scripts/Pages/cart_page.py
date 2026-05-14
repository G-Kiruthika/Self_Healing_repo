from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Page Object Model for Cart Page.
    Implements cart operations and validations for e-commerce application.
    Strictly follows Selenium Python automation best practices.
    """

    # Locators
    PRODUCT_A_ROW = (By.XPATH, "//tr[td[contains(text(),'Product A')]]")
    PRODUCT_C_ROW = (By.XPATH, "//tr[td[contains(text(),'Product C')]]")
    DELETE_BUTTON_PRODUCT_C = (By.XPATH, "//tr[td[contains(text(),'Product C')]]//button[contains(text(),'Delete')]")
    CART_TOTAL = (By.ID, "cart-total")
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(),'Your cart is empty')]")
    RETURN_TO_CATALOG_BUTTON = (By.XPATH, "//button[contains(text(),'Return to Product Catalog')]")

    def __init__(self, driver):
        super().__init__(driver)

    def ensure_product_in_cart(self, product_name, subtotal):
        """
        Ensures a product is present in the cart with the specified subtotal.
        
        Args:
            product_name (str): Name of the product
            subtotal (str): Expected subtotal for the product
        """
        product_locator = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]")
        self.wait_for_element_visible(product_locator)

    def click_delete_button(self, product_name):
        """
        Clicks the delete button for the specified product.
        
        Args:
            product_name (str): Name of the product to delete
        """
        delete_button = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]//button[contains(text(),'Delete')]")
        self.click_element(delete_button)

    def navigate_to_cart_page(self):
        """
        Navigates to the cart page.
        """
        # Implementation depends on application navigation
        # This is a placeholder for navigation logic
        pass

    def observe_cart_page(self):
        """
        Observes the cart page to ensure it is loaded.
        """
        self.wait_for_element_visible(self.CART_TOTAL)

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

    def validate_product_not_present(self, product_name):
        """
        Validates that a product is not present in the cart.
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            bool: True if product is not present, False otherwise
        """
        product_locator = (By.XPATH, f"//tr[td[contains(text(),'{product_name}')]]")
        return not self.is_element_visible(product_locator)

    def validate_cart_total(self, expected_total):
        """
        Validates the cart total matches the expected value.
        
        Args:
            expected_total (str): Expected cart total
            
        Returns:
            bool: True if total matches, False otherwise
        """
        cart_total_element = self.find_element(self.CART_TOTAL)
        actual_total = cart_total_element.text.strip()
        return expected_total in actual_total

    def validate_cart_empty_message(self):
        """
        Validates that the empty cart message is displayed.
        
        Returns:
            bool: True if empty cart message is visible, False otherwise
        """
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)

    def validate_no_line_items(self):
        """
        Validates that there are no line items in the cart.
        
        Returns:
            bool: True if no line items are present, False otherwise
        """
        line_items = self.driver.find_elements(By.XPATH, "//tr[@class='cart-item']")
        return len(line_items) == 0
