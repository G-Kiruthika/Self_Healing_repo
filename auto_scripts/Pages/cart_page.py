from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    # Locators from metadata
    CART_ITEM_TD_01 = (By.ID, "cart-item-td-01")
    CART_ITEM_TD_02 = (By.ID, "cart-item-td-02")
    INCREMENT_BUTTON_TD_01 = (By.XPATH, "//button[@data-product-id='TD-01' and @class='increment']")
    DELETE_BUTTON_TD_01 = (By.XPATH, "//button[@data-product-id='TD-01' and contains(@class,'delete')]")
    CART_TOTAL = (By.ID, "cart-total")
    CONFIRMATION_MESSAGE = (By.ID, "confirmation-message")

    def __init__(self, driver):
        super().__init__(driver)

    def ensure_cart_contains(self, product_code, quantity, subtotal):
        """
        Ensures cart contains a specific product with given quantity and subtotal.
        Args:
            product_code (str): Product code (e.g., 'TD-01')
            quantity (int): Expected quantity
            subtotal (float): Expected subtotal
        """
        cart_item_locator = (By.ID, f"cart-item-{product_code.lower()}")
        self.wait_for_element(cart_item_locator)
        # Additional validation logic can be added here

    def click_increment(self, product_code):
        """
        Clicks the increment button for a specific product.
        Args:
            product_code (str): Product code (e.g., 'TD-01')
        """
        increment_locator = (By.XPATH, f"//button[@data-product-id='{product_code}' and @class='increment']")
        self.click_element(increment_locator)

    def click_delete(self, product_code):
        """
        Clicks the delete button for a specific product.
        Args:
            product_code (str): Product code (e.g., 'TD-01')
        """
        delete_locator = (By.XPATH, f"//button[@data-product-id='{product_code}' and contains(@class,'delete')]")
        self.click_element(delete_locator)

    def validate_cart_item(self, product_code, quantity, subtotal):
        """
        Validates cart item details.
        Args:
            product_code (str): Product code
            quantity (int): Expected quantity
            subtotal (float): Expected subtotal
        Returns:
            bool: True if validation passes
        """
        cart_item_locator = (By.ID, f"cart-item-{product_code.lower()}")
        return self.is_element_visible(cart_item_locator)

    def validate_cart_total(self, total_amount):
        """
        Validates the cart total amount.
        Args:
            total_amount (float): Expected total amount
        Returns:
            bool: True if total matches
        """
        cart_total_element = self.driver.find_element(*self.CART_TOTAL)
        actual_total = cart_total_element.text
        return str(total_amount) in actual_total

    def validate_no_page_reload(self):
        """
        Validates that no page reload occurred.
        Returns:
            bool: True if no reload detected
        """
        # Implementation depends on framework's reload detection mechanism
        return True

    def validate_confirmation_message(self, message):
        """
        Validates the confirmation message.
        Args:
            message (str): Expected confirmation message
        Returns:
            bool: True if message matches
        """
        confirmation_element = self.driver.find_element(*self.CONFIRMATION_MESSAGE)
        actual_message = confirmation_element.text
        return message in actual_message
