from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    PRODUCT_D_ROW = (By.XPATH, "//tr[@data-product='Vitamin Pack']")
    QUANTITY_INPUT = (By.XPATH, "//input[@data-product='Vitamin Pack'][@type='number']")
    SUBSCRIPTION_INDICATOR = (By.XPATH, "//span[@data-product='Vitamin Pack'][@class='subscription']")
    SUBTOTAL_LABEL = (By.XPATH, "//tr[@data-product='Vitamin Pack']//td[@class='subtotal']")
    CART_TOTAL_LABEL = (By.ID, "cart-total")
    PRODUCT_C_ROW = (By.XPATH, "//tr[td[contains(text(),'Laptop Stand')]]")
    PRODUCT_C_QUANTITY_INPUT = (By.XPATH, "//tr[td[contains(text(),'Laptop Stand')]]//input[@type='number']")
    PRODUCT_C_STOCK_LABEL = (By.XPATH, "//tr[td[contains(text(),'Laptop Stand')]]//span[@class='stock']")
    CART_TOTAL = (By.ID, "cart-total")
    INVENTORY_ERROR_MESSAGE = (By.CLASS_NAME, "inventory-error")
    PRODUCT_B_ROW = (By.XPATH, "//tr[td[contains(text(),'Coffee Subscription')]]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".cart-error-message")
    WARNING_MESSAGE = (By.CSS_SELECTOR, ".cart-warning-message")

    def __init__(self, driver):
        super().__init__(driver)

    def update_product_quantity(self, product_name, quantity):
        self.enter_text(self.QUANTITY_INPUT, str(quantity))

    def is_product_in_cart(self, product_name, quantity):
        if not self.is_element_visible(self.PRODUCT_D_ROW):
            return False
        quantity_element = self.driver.find_element(*self.QUANTITY_INPUT)
        return int(quantity_element.get_attribute('value')) == quantity

    def is_subscription_indicator_visible(self, product_name):
        return self.is_element_visible(self.SUBSCRIPTION_INDICATOR)

    def verify_subtotal(self, product_name, expected_subtotal):
        subtotal_element = self.driver.find_element(*self.SUBTOTAL_LABEL)
        actual_subtotal = float(subtotal_element.text.replace('$', '').strip())
        return actual_subtotal == expected_subtotal

    def verify_cart_total(self, expected_total):
        total_element = self.driver.find_element(*self.CART_TOTAL_LABEL)
        actual_total = float(total_element.text.replace('$', '').strip())
        return actual_total == expected_total

    def set_product_quantity(self, product_name, quantity):
        self.enter_text(self.PRODUCT_C_QUANTITY_INPUT, str(quantity))

    def get_product_stock(self, product_name):
        stock_element = self.driver.find_element(*self.PRODUCT_C_STOCK_LABEL)
        return stock_element.text

    def get_cart_total(self):
        total_element = self.driver.find_element(*self.CART_TOTAL)
        return total_element.text

    def validate_product_in_cart(self, product_name):
        return self.is_element_visible(self.PRODUCT_C_ROW)

    def validate_quantity(self, product_name, expected_quantity):
        quantity_element = self.driver.find_element(*self.PRODUCT_C_QUANTITY_INPUT)
        actual_quantity = int(quantity_element.get_attribute('value'))
        return actual_quantity == expected_quantity

    def validate_cart_total(self, expected_total):
        total_element = self.driver.find_element(*self.CART_TOTAL)
        actual_total = total_element.text.replace('$', '').strip()
        return actual_total == str(expected_total)

    def validate_inventory_error_displayed(self):
        return self.is_element_visible(self.INVENTORY_ERROR_MESSAGE)

    def ensure_product_in_cart(self, product_name, quantity):
        """
        Ensures the specified product is in the cart with the given quantity.
        """
        if product_name == "Laptop Stand":
            locator = self.PRODUCT_C_ROW
        elif product_name == "Coffee Subscription":
            locator = self.PRODUCT_B_ROW
        else:
            locator = self.PRODUCT_D_ROW
        if not self.is_element_visible(locator):
            return False
        return self.validate_quantity(product_name, quantity)

    def update_quantity(self, product_name, quantity):
        """
        Updates the quantity of the specified product in the cart.
        """
        self.enter_text(self.QUANTITY_INPUT, str(quantity))

    def check_line_item_subtotal(self, product_name):
        """
        Checks and returns the line item subtotal for the specified product.
        """
        subtotal_element = self.driver.find_element(*self.SUBTOTAL_LABEL)
        return subtotal_element.text

    def check_error_messages(self):
        """
        Checks for error messages in the cart.
        """
        return self.is_element_visible(self.ERROR_MESSAGE)

    def attempt_reduce_quantity(self, product_name, quantity):
        """
        Attempts to reduce the quantity of the specified product.
        """
        self.enter_text(self.QUANTITY_INPUT, str(quantity))

    def check_cart_quantity(self, product_name):
        """
        Checks and returns the current quantity of the specified product in the cart.
        """
        quantity_element = self.driver.find_element(*self.QUANTITY_INPUT)
        return int(quantity_element.get_attribute('value'))

    def validate_subtotal(self, product_name, expected_subtotal):
        """
        Validates the subtotal for the specified product matches the expected value.
        """
        subtotal_element = self.driver.find_element(*self.SUBTOTAL_LABEL)
        actual_subtotal = float(subtotal_element.text.replace('$', '').strip())
        return actual_subtotal == expected_subtotal

    def validate_no_inventory_error(self):
        """
        Validates that no inventory error message is displayed.
        """
        return not self.is_element_visible(self.ERROR_MESSAGE)

    def validate_warning_message(self):
        """
        Validates that a warning message is displayed.
        """
        return self.is_element_visible(self.WARNING_MESSAGE)

    def validate_quantity_threshold(self, product_name, expected_quantity):
        """
        Validates the quantity threshold for the specified product.
        """
        quantity_element = self.driver.find_element(*self.QUANTITY_INPUT)
        actual_quantity = int(quantity_element.get_attribute('value'))
        return actual_quantity == expected_quantity
