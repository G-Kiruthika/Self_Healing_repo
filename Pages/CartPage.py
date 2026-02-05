# CartPage.py
# Page Object for Cart-related operations

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class CartPage:
    """
    Page Object Model for Cart-related actions.

    Methods:
        add_product_to_cart(product_id: str, quantity: int) -> bool
            Attempts to add a product to the cart by product ID and quantity.
            Returns True if successful, False if product not found or error occurs.
    """
    def __init__(self, driver):
        """
        Initialize CartPage with driver and define locators.
        """
        self.driver = driver
        # Locators (Assumed; update with actual values as needed)
        self.product_id_field = (By.ID, "product_id")
        self.quantity_field = (By.ID, "quantity")
        self.add_to_cart_button = (By.ID, "add_to_cart")
        self.error_message = (By.ID, "cart_error_message")

    def add_product_to_cart(self, product_id, quantity):
        """
        Attempts to add a product to the cart using given product_id and quantity.
        Returns True if product is added, False if error message is displayed (e.g., invalid product ID).
        """
        try:
            self.driver.find_element(*self.product_id_field).clear()
            self.driver.find_element(*self.product_id_field).send_keys(product_id)
            self.driver.find_element(*self.quantity_field).clear()
            self.driver.find_element(*self.quantity_field).send_keys(str(quantity))
            self.driver.find_element(*self.add_to_cart_button).click()
            # Check for error message
            try:
                error = self.driver.find_element(*self.error_message)
                if error.is_displayed():
                    return False
            except NoSuchElementException:
                # No error message, assume add to cart succeeded
                return True
        except Exception as e:
            # Log exception if needed
            return False
