from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    # Locators
    PRODUCT_ROW = (By.XPATH, "//tr[@data-product-id]")
    QUANTITY_FIELD = (By.CSS_SELECTOR, ".quantity-input")
    DECREMENT_BUTTON = (By.CSS_SELECTOR, ".decrement-btn")
    VALIDATION_ERROR_MESSAGE = (By.CSS_SELECTOR, ".validation-error")
    DELETE_BUTTON = (By.XPATH, "//button[@data-action='delete']")
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(),'Your cart is empty')]")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//button[text()='Continue Shopping']")
    CHECKOUT_BUTTON = (By.XPATH, "//button[text()='Checkout']")
    QUANTITY_INPUT = (By.XPATH, "//input[@name='quantity']")
    INVENTORY_ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'error') and contains(text(),'units available')]")
    SUGGESTION_MESSAGE = (By.XPATH, "//div[contains(text(),'Maximum available')]")

    def __init__(self, driver):
        super().__init__(driver)

    def click_decrement(self, product_id):
        """
        Clicks the decrement button for a specific product.
        Args:
            product_id (str): Product ID
        """
        decrement_locator = (By.XPATH, f"//tr[@data-product-id='{product_id}']//button[contains(@class,'decrement-btn')]")
        self.click_element(decrement_locator)

    def is_product_quantity_displayed(self, product_id, quantity):
        """
        Validates if the product quantity matches the expected value.
        Args:
            product_id (str): Product ID
            quantity (int): Expected quantity
        Returns:
            bool: True if quantity matches, False otherwise
        """
        quantity_locator = (By.XPATH, f"//tr[@data-product-id='{product_id}']//input[contains(@class,'quantity-input')]")
        try:
            quantity_element = self.driver.find_element(*quantity_locator)
            actual_quantity = quantity_element.get_attribute('value')
            return int(actual_quantity) == quantity
        except Exception:
            return False

    def is_minimum_threshold_displayed(self, product_id, threshold):
        """
        Validates if the minimum threshold message is displayed for a product.
        Args:
            product_id (str): Product ID
            threshold (int): Minimum threshold value
        Returns:
            bool: True if threshold message is displayed, False otherwise
        """
        threshold_locator = (By.XPATH, f"//tr[@data-product-id='{product_id}']//span[contains(text(),'Minimum quantity is {threshold}')]")
        return self.is_element_visible(threshold_locator)

    def is_validation_error_displayed(self):
        """
        Validates if a validation error message is displayed.
        Returns:
            bool: True if validation error is visible, False otherwise
        """
        return self.is_element_visible(self.VALIDATION_ERROR_MESSAGE)

    def is_quantity_unchanged(self, product_id, quantity):
        """
        Validates if the product quantity remains unchanged.
        Args:
            product_id (str): Product ID
            quantity (int): Expected unchanged quantity
        Returns:
            bool: True if quantity is unchanged, False otherwise
        """
        return self.is_product_quantity_displayed(product_id, quantity)

    def is_decrement_button_disabled(self, product_id):
        """
        Validates if the decrement button is disabled for a product.
        Args:
            product_id (str): Product ID
        Returns:
            bool: True if button is disabled, False otherwise
        """
        decrement_locator = (By.XPATH, f"//tr[@data-product-id='{product_id}']//button[contains(@class,'decrement-btn')]")
        try:
            button = self.driver.find_element(*decrement_locator)
            return not button.is_enabled() or button.get_attribute("disabled") is not None
        except Exception:
            return False

    def delete_product(self, product_id):
        """
        Deletes a product from the cart.
        Args:
            product_id (str): Product ID to delete
        """
        delete_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//button[@data-action='delete']")
        self.click_element(delete_locator)

    def click_continue_shopping(self):
        """
        Clicks the Continue Shopping button.
        """
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)

    def update_quantity(self, product_id, quantity):
        """
        Updates the quantity for a specific product.
        Args:
            product_id (str): Product ID
            quantity (int): New quantity value
        """
        quantity_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//input[@name='quantity']")
        self.enter_text(quantity_locator, str(quantity))

    def is_product_in_cart(self, product_id):
        """
        Validates if a product is present in the cart.
        Args:
            product_id (str): Product ID
        Returns:
            bool: True if product is in cart, False otherwise
        """
        product_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']")
        return self.is_element_visible(product_locator)

    def is_cart_empty(self):
        """
        Validates if the cart is empty.
        Returns:
            bool: True if cart is empty, False otherwise
        """
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)

    def is_empty_cart_message_displayed(self):
        """
        Validates if the empty cart message is displayed.
        Returns:
            bool: True if message is displayed, False otherwise
        """
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)

    def is_continue_shopping_button_displayed(self):
        """
        Validates if the Continue Shopping button is displayed.
        Returns:
            bool: True if button is displayed, False otherwise
        """
        return self.is_element_visible(self.CONTINUE_SHOPPING_BUTTON)

    def is_checkout_button_unavailable(self):
        """
        Validates if the Checkout button is unavailable.
        Returns:
            bool: True if button is unavailable, False otherwise
        """
        return not self.is_element_visible(self.CHECKOUT_BUTTON)

    def is_inventory_error_displayed(self):
        """
        Validates if the inventory error message is displayed.
        Returns:
            bool: True if error is displayed, False otherwise
        """
        return self.is_element_visible(self.INVENTORY_ERROR_MESSAGE)

    def is_quantity_equal(self, product_id, expected_quantity):
        """
        Validates if the quantity for a product matches the expected value.
        Args:
            product_id (str): Product ID
            expected_quantity (int): Expected quantity value
        Returns:
            bool: True if quantity matches, False otherwise
        """
        quantity_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//input[@name='quantity']")
        actual_quantity = self.driver.find_element(*quantity_locator).get_attribute('value')
        return int(actual_quantity) == expected_quantity

    def is_suggestion_message_displayed(self):
        """
        Validates if the suggestion message is displayed.
        Returns:
            bool: True if message is displayed, False otherwise
        """
        return self.is_element_visible(self.SUGGESTION_MESSAGE)
