# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.cart_icon = (By.ID, 'cart-icon')
        self.cart_item_quantity = (By.XPATH, "//div[@class='cart-item' and @data-product-id='12345']//input[@class='cart-quantity']")
        self.cart_error_message = (By.CSS_SELECTOR, '.cart-error-message')
        self.stock_warning_message = (By.XPATH, "//div[contains(@class, 'stock-warning') or contains(@class, 'error-message')]")
        # Embedded locators due to absence of central Locators.json
        self.delete_cart_button = (By.ID, 'delete-cart-btn')  # Example locator for Delete Cart button
        self.cart_not_found_message = (By.CSS_SELECTOR, '.cart-not-found-message')  # Example locator for cart absence
        self.cart_container = (By.ID, 'cart-container')  # Example locator for cart container

    def open_cart(self):
        self.driver.find_element(*self.cart_icon).click()

    def get_cart_quantity(self):
        return self.driver.find_element(*self.cart_item_quantity).get_attribute('value')

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.cart_error_message).text
        except:
            return None

    def get_stock_warning(self):
        try:
            return self.driver.find_element(*self.stock_warning_message).text
        except:
            return None

    def delete_cart(self):
        """
        Deletes the shopping cart by clicking the delete button.
        """
        try:
            self.driver.find_element(*self.delete_cart_button).click()
        except NoSuchElementException:
            raise Exception("Delete Cart button not found on CartPage.")

    def is_cart_deleted(self):
        """
        Verifies if the cart is deleted by checking for a 'cart not found' message or absence of cart container.
        Returns True if cart is deleted, False otherwise.
        """
        try:
            # Check for cart not found message
            if self.driver.find_element(*self.cart_not_found_message):
                return True
        except NoSuchElementException:
            pass
        try:
            # Check if cart container is absent
            self.driver.find_element(*self.cart_container)
            return False
        except NoSuchElementException:
            return True
        return False
