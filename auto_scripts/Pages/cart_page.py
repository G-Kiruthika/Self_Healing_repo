from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    PRODUCT_D_ROW = (By.XPATH, "//tr[@data-product='Vitamin Pack']")
    QUANTITY_INPUT = (By.XPATH, "//input[@data-product='Vitamin Pack'][@type='number']")
    SUBSCRIPTION_INDICATOR = (By.XPATH, "//span[@data-product='Vitamin Pack'][@class='subscription']")
    SUBTOTAL_LABEL = (By.XPATH, "//tr[@data-product='Vitamin Pack']//td[@class='subtotal']")
    CART_TOTAL_LABEL = (By.ID, "cart-total")

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