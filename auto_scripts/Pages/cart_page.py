from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ICON = (By.ID, "cart-icon")
    CART_ITEM_COUNT = (By.XPATH, "//span[@id='cart-count']")
    PRODUCT_SUBTOTAL = (By.XPATH, "//tr[@data-product]//td[@class='subtotal']")

    def __init__(self, driver):
        super().__init__(driver)

    def open_cart(self):
        self.click_element(self.CART_ICON)

    def get_cart_item_count(self):
        count_element = self.driver.find_element(*self.CART_ITEM_COUNT)
        return int(count_element.text)

    def get_product_subtotal(self, product_name):
        subtotal_locator = (By.XPATH, f"//tr[@data-product='{product_name}']//td[@class='subtotal']")
        subtotal_element = self.driver.find_element(*subtotal_locator)
        return float(subtotal_element.text.replace('$', ''))

    def is_cart_item_count(self, count):
        return self.get_cart_item_count() == count

    def is_product_subtotal(self, product_name, expected_subtotal):
        actual_subtotal = self.get_product_subtotal(product_name)
        return actual_subtotal == expected_subtotal