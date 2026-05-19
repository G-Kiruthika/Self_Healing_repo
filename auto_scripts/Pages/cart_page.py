from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    PRODUCT_A_ROW = (By.XPATH, "//tr[.//td[contains(text(),'Wireless Mouse')]]")
    DELETE_BUTTON_PRODUCT_A = (By.XPATH, "//tr[.//td[contains(text(),'Wireless Mouse')]]//button[contains(text(),'Delete')]")
    CART_EMPTY_MESSAGE = (By.XPATH, "//*[contains(text(),'Your cart is empty')]")
    RETURN_TO_CATALOG_BUTTON = (By.XPATH, "//button[contains(text(),'Return to product catalog')]")
    CART_TOTAL = (By.XPATH, "//span[@id='cart-total']")
    PRODUCT_B_ROW = (By.XPATH, "//tr[.//td[contains(text(),'Product B')]]")
    PRODUCT_C_ROW = (By.XPATH, "//tr[.//td[contains(text(),'Product C')]]")
    LINE_ITEM_SUBTOTAL = (By.XPATH, "//td[@class='subtotal']")
    PRODUCT_D_ROW = (By.XPATH, "//tr[@data-product='Vitamin Pack']")
    QUANTITY_INPUT = (By.XPATH, "//input[@data-product='Vitamin Pack'][@type='number']")
    SUBSCRIPTION_INDICATOR = (By.XPATH, "//span[@data-product='Vitamin Pack'][@class='subscription']")
    SUBTOTAL_LABEL = (By.XPATH, "//tr[@data-product='Vitamin Pack']//td[@class='subtotal']")
    CART_TOTAL_LABEL = (By.ID, "cart-total")
    PRODUCT_C_QUANTITY_INPUT = (By.XPATH, "//tr[td[contains(text(),'Laptop Stand')]]//input[@type='number']")
    PRODUCT_C_STOCK_LABEL = (By.XPATH, "//tr[td[contains(text(),'Laptop Stand')]]//span[@class='stock']")
    INVENTORY_ERROR_MESSAGE = (By.CLASS_NAME, "inventory-error")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".cart-error-message")
    WARNING_MESSAGE = (By.CSS_SELECTOR, ".cart-warning-message")

    def __init__(self, driver):
        super().__init__(driver)

    def click_delete_button(self, product_name):
        if product_name == "Wireless Mouse":
            self.click_element(self.DELETE_BUTTON_PRODUCT_A)
        else:
            locator = (By.XPATH, f"//tr[.//td[contains(text(),'{product_name}')]]//button[contains(text(),'Delete')]")
            self.click_element(locator)

    def navigate_to_cart_page(self):
        self.driver.get("https://example-ecommerce.com/cart")

    def is_product_in_cart(self, product_name):
        if product_name == "Wireless Mouse":
            return self.is_element_visible(self.PRODUCT_A_ROW)
        elif product_name == "Product B":
            return self.is_element_visible(self.PRODUCT_B_ROW)
        elif product_name == "Product C":
            return self.is_element_visible(self.PRODUCT_C_ROW)
        else:
            locator = (By.XPATH, f"//tr[.//td[contains(text(),'{product_name}')]]")
            return self.is_element_visible(locator)

    def is_cart_empty(self):
        return self.is_element_visible(self.CART_EMPTY_MESSAGE)

    def is_cart_total(self, expected_total):
        total_element = self.driver.find_element(*self.CART_TOTAL)
        actual_total = total_element.text.replace('$', '').strip()
        return actual_total == str(expected_total)

    def is_line_item_subtotal_correct(self, product_name, expected_subtotal):
        subtotal_element = self.driver.find_element(*self.LINE_ITEM_SUBTOTAL)
        actual_subtotal = float(subtotal_element.text.replace('$', '').strip())
        return actual_subtotal == expected_subtotal

    def update_product_quantity(self, product_name, quantity):
        self.enter_text(self.QUANTITY_INPUT, str(quantity))

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
        self.enter_text(self.QUANTITY_INPUT, str(quantity))

    def check_line_item_subtotal(self, product_name):
        subtotal_element = self.driver.find_element(*self.SUBTOTAL_LABEL)
        return subtotal_element.text

    def check_error_messages(self):
        return self.is_element_visible(self.ERROR_MESSAGE)

    def attempt_reduce_quantity(self, product_name, quantity):
        self.enter_text(self.QUANTITY_INPUT, str(quantity))

    def check_cart_quantity(self, product_name):
        quantity_element = self.driver.find_element(*self.QUANTITY_INPUT)
        return int(quantity_element.get_attribute('value'))

    def validate_subtotal(self, product_name, expected_subtotal):
        subtotal_element = self.driver.find_element(*self.SUBTOTAL_LABEL)
        actual_subtotal = float(subtotal_element.text.replace('$', '').strip())
        return actual_subtotal == expected_subtotal

    def validate_no_inventory_error(self):
        return not self.is_element_visible(self.ERROR_MESSAGE)

    def validate_warning_message(self):
        return self.is_element_visible(self.WARNING_MESSAGE)

    def validate_quantity_threshold(self, product_name, expected_quantity):
        quantity_element = self.driver.find_element(*self.QUANTITY_INPUT)
        actual_quantity = int(quantity_element.get_attribute('value'))
        return actual_quantity == expected_quantity
