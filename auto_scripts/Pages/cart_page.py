from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEM_TD_03 = (By.XPATH, "//div[@data-sku='TD-03']")
    CART_ITEM_TD_01 = (By.XPATH, "//div[@data-sku='TD-01']")
    QUANTITY_INPUT = (By.XPATH, "//input[@class='cart-qty']")
    INCREMENT_BUTTON = (By.XPATH, "//button[@aria-label='Increment']")
    MAX_QUANTITY_MESSAGE = (By.XPATH, "//div[contains(text(),'Maximum available quantity reached')]")
    SUBTOTAL = (By.XPATH, "//span[@class='line-item-subtotal']")
    CONFIRMATION_MESSAGE = (By.XPATH, "//div[contains(text(),'Quantity updated in cart')]")

    def __init__(self, driver):
        super().__init__(driver)

    def set_cart_item_quantity(self, sku, quantity):
        """
        Sets the quantity for a cart item by SKU.
        Args:
            sku (str): Product SKU
            quantity (int): Quantity to set
        """
        quantity_locator = (By.XPATH, f"//div[@data-sku='{sku}']//input[@class='cart-qty']")
        self.enter_text(quantity_locator, str(quantity))

    def increment_quantity(self, sku):
        """
        Increments the quantity for a cart item by SKU.
        Args:
            sku (str): Product SKU
        """
        increment_locator = (By.XPATH, f"//div[@data-sku='{sku}']//button[@aria-label='Increment']")
        self.click_element(increment_locator)

    def navigate_to_cart(self):
        """
        Navigates to the cart page.
        """
        self.driver.get("https://example-ecommerce.com/cart")
        self.wait_for_page_load()

    def verify_cart_item_quantity(self, sku, expected_quantity):
        """
        Verifies the quantity of a cart item by SKU.
        Args:
            sku (str): Product SKU
            expected_quantity (int): Expected quantity
        Returns:
            bool: True if quantity matches, False otherwise
        """
        quantity_locator = (By.XPATH, f"//div[@data-sku='{sku}']//input[@class='cart-qty']")
        try:
            quantity_elem = self.driver.find_element(*quantity_locator)
            actual_quantity = int(quantity_elem.get_attribute('value'))
            return actual_quantity == expected_quantity
        except Exception:
            return False

    def verify_increment_button_disabled(self, sku):
        """
        Verifies if the increment button is disabled for a cart item by SKU.
        Args:
            sku (str): Product SKU
        Returns:
            bool: True if button is disabled, False otherwise
        """
        increment_locator = (By.XPATH, f"//div[@data-sku='{sku}']//button[@aria-label='Increment']")
        try:
            button = self.driver.find_element(*increment_locator)
            return not button.is_enabled() or button.get_attribute("disabled") is not None
        except Exception:
            return False

    def verify_max_quantity_message_displayed(self):
        """
        Verifies if the maximum quantity message is displayed.
        Returns:
            bool: True if message is displayed, False otherwise
        """
        return self.is_element_visible(self.MAX_QUANTITY_MESSAGE)

    def verify_line_item_subtotal(self, sku, expected_subtotal):
        """
        Verifies the line item subtotal for a cart item by SKU.
        Args:
            sku (str): Product SKU
            expected_subtotal (str): Expected subtotal
        Returns:
            bool: True if subtotal matches, False otherwise
        """
        subtotal_locator = (By.XPATH, f"//div[@data-sku='{sku}']//span[@class='line-item-subtotal']")
        try:
            subtotal_elem = self.driver.find_element(*subtotal_locator)
            return expected_subtotal in subtotal_elem.text
        except Exception:
            return False

    def verify_confirmation_message_displayed(self):
        """
        Verifies if the confirmation message is displayed.
        Returns:
            bool: True if message is displayed, False otherwise
        """
        return self.is_element_visible(self.CONFIRMATION_MESSAGE)
