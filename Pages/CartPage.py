# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.cart_icon = (By.ID, 'cart-icon')
        self.cart_item_quantity = (By.XPATH, "//div[@class='cart-item' and @data-product-id='12345']//input[@class='cart-quantity']")
        self.cart_error_message = (By.CSS_SELECTOR, '.cart-error-message')
        self.stock_warning_message = (By.XPATH, "//div[contains(@class, 'stock-warning') or contains(@class, 'error-message')]")

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
