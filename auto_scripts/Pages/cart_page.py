from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    # Locators from metadata
    PRODUCT_NAME = (By.XPATH, "//div[@class='cart-item']//span[@class='product-name']")
    UNIT_PRICE = (By.XPATH, "//div[@class='cart-item']//span[@class='unit-price']")
    QUANTITY_FIELD = (By.XPATH, "//input[@name='quantity']")
    SUBTOTAL = (By.XPATH, "//div[@class='cart-item']//span[@class='subtotal']")
    CART_TOTAL = (By.XPATH, "//span[@id='cart-total']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='alert-success']")
    
    # Existing locators
    PRODUCT_ROW = (By.XPATH, "//tr[@data-product-id]")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".quantity-input")
    DECREMENT_BUTTON = (By.CSS_SELECTOR, ".decrement-btn")
    VALIDATION_ERROR_MESSAGE = (By.CSS_SELECTOR, ".validation-error")
    DELETE_BUTTON = (By.XPATH, "//button[@data-action='delete']")
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(),'Your cart is empty')]")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//button[text()='Continue Shopping']")
    CHECKOUT_BUTTON = (By.XPATH, "//button[text()='Checkout']")
    INVENTORY_ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'error') and contains(text(),'units available')]")
    SUGGESTION_MESSAGE = (By.XPATH, "//div[contains(text(),'Maximum available')]")
    UPDATE_BUTTON = (By.XPATH, "//button[@id='update-cart']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_cart(self):
        """
        Navigates to the cart page.
        """
        self.driver.get("https://example-ecommerce.com/cart")
        self.wait_for_page_load()

    def update_quantity(self, product_name, quantity):
        """
        Updates the quantity for a specific product by product name.
        Args:
            product_name (str): Product name
            quantity (int): New quantity value
        """
        quantity_locator = (By.XPATH, f"//div[contains(@class,'cart-item')]//span[@class='product-name' and text()='{product_name}']/ancestor::div[@class='cart-item']//input[@name='quantity']")
        self.enter_text(quantity_locator, str(quantity))

    def enter_quantity(self, quantity):
        """
        Enters quantity in the quantity field.
        Args:
            quantity (int): Quantity value to enter
        """
        self.enter_text(self.QUANTITY_FIELD, str(quantity))

    def click_update_button(self):
        """
        Clicks the update cart button.
        """
        self.click_element(self.UPDATE_BUTTON)

    def verify_products_in_cart(self, product_list):
        """
        Verifies that all products in the list are present in the cart.
        Args:
            product_list (list): List of product names to verify
        Returns:
            bool: True if all products are in cart, False otherwise
        """
        for product in product_list:
            product_locator = (By.XPATH, f"//div[@class='cart-item']//span[@class='product-name' and text()='{product}']")
            if not self.is_element_visible(product_locator):
                return False
        return True

    def verify_product_fields(self, product_name, unit_price, quantity, subtotal):
        """
        Verifies product fields for a specific product.
        Args:
            product_name (str): Product name
            unit_price (str): Expected unit price
            quantity (str): Expected quantity
            subtotal (str): Expected subtotal
        Returns:
            bool: True if all fields match, False otherwise
        """
        try:
            product_row = (By.XPATH, f"//div[@class='cart-item']//span[@class='product-name' and text()='{product_name}']/ancestor::div[@class='cart-item']")
            if not self.is_element_visible(product_row):
                return False
            
            unit_price_elem = self.driver.find_element(By.XPATH, f"//div[@class='cart-item']//span[@class='product-name' and text()='{product_name}']/ancestor::div[@class='cart-item']//span[@class='unit-price']")
            quantity_elem = self.driver.find_element(By.XPATH, f"//div[@class='cart-item']//span[@class='product-name' and text()='{product_name}']/ancestor::div[@class='cart-item']//input[@name='quantity']")
            subtotal_elem = self.driver.find_element(By.XPATH, f"//div[@class='cart-item']//span[@class='product-name' and text()='{product_name}']/ancestor::div[@class='cart-item']//span[@class='subtotal']")
            
            return (unit_price_elem.text == unit_price and 
                    quantity_elem.get_attribute('value') == str(quantity) and 
                    subtotal_elem.text == subtotal)
        except Exception:
            return False

    def verify_cart_total(self, expected_total):
        """
        Verifies the cart total matches the expected value.
        Args:
            expected_total (str): Expected cart total
        Returns:
            bool: True if cart total matches, False otherwise
        """
        try:
            cart_total_elem = self.driver.find_element(*self.CART_TOTAL)
            return cart_total_elem.text == expected_total
        except Exception:
            return False

    def verify_success_message(self, message):
        """
        Verifies the success message is displayed with expected text.
        Args:
            message (str): Expected success message
        Returns:
            bool: True if message matches, False otherwise
        """
        try:
            success_elem = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return message in success_elem.text
        except Exception:
            return False

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
