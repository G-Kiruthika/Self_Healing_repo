from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.cart_button = (By.CSS_SELECTOR, '#cart-btn')
        self.add_to_cart_button = (By.CSS_SELECTOR, '.add-to-cart')
        self.cart_item_list = (By.CSS_SELECTOR, '#cart-items')
        # API URL is present but not used in Selenium context

    def open_cart(self):
        self.driver.find_element(*self.cart_button).click()

    def add_product_to_cart(self, product_id: str, quantity: int):
        # This method assumes that the product element can be found by a data attribute
        try:
            product_elem = self.driver.find_element(By.CSS_SELECTOR, f"[data-product-id='{product_id}']")
            qty_input = product_elem.find_element(By.CSS_SELECTOR, 'input[type="number"]')
            qty_input.clear()
            qty_input.send_keys(str(quantity))
            add_btn = product_elem.find_element(*self.add_to_cart_button)
            add_btn.click()
        except NoSuchElementException:
            raise Exception(f"Product with id {product_id} not found on page.")

    def is_error_displayed(self):
        # Checks for an error message after attempting to add zero quantity
        try:
            error_elem = self.driver.find_element(By.CSS_SELECTOR, '.error-message')
            return error_elem.is_displayed()
        except NoSuchElementException:
            return False

    def validate_add_zero_quantity(self, product_id: str):
        self.add_product_to_cart(product_id, 0)
        return self.is_error_displayed()
