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
        # Added selectors for cart deletion and verification
        self.delete_cart_button = (By.XPATH, "//button[@id='delete-cart' and @data-cart-id='{cart_id}']")
        self.cart_container = (By.XPATH, "//div[@class='cart-container' and @data-cart-id='{cart_id}']")

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

    # --- ADDED for TC_CART_007 ---
    def delete_cart(self, cart_id: str):
        """
        Deletes the shopping cart for the given cart_id.
        """
        try:
            delete_button_locator = (self.delete_cart_button[0], self.delete_cart_button[1].format(cart_id=cart_id))
            self.driver.find_element(*delete_button_locator).click()
            # Optionally, handle confirmation dialog
            try:
                confirm_button = self.driver.find_element(By.XPATH, "//button[@id='confirm-delete-cart']")
                confirm_button.click()
            except NoSuchElementException:
                pass
        except NoSuchElementException:
            raise Exception(f"Delete button for cart_id {cart_id} not found.")

    def is_cart_deleted(self, cart_id: str) -> bool:
        """
        Returns True if the cart is deleted (not found), False otherwise.
        """
        try:
            cart_locator = (self.cart_container[0], self.cart_container[1].format(cart_id=cart_id))
            self.driver.find_element(*cart_locator)
            return False
        except NoSuchElementException:
            return True
