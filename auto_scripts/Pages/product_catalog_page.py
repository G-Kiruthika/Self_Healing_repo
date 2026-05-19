from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    PRODUCT_D_CARD = (By.XPATH, "//div[@data-product='Vitamin Pack']")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[@data-product='Vitamin Pack'][text()='Add to Cart']")
    PRODUCT_E_ROW = (By.XPATH, "//tr[td[contains(text(),'USB Cable')]]")
    PRODUCT_E_STOCK_LABEL = (By.XPATH, "//tr[td[contains(text(),'USB Cable')]]//span[@class='stock']")
    ADD_TO_CART_BUTTON_E = (By.XPATH, "//tr[td[contains(text(),'USB Cable')]]//button[contains(text(),'Add to Cart')]")
    INVENTORY_ERROR_MESSAGE = (By.CLASS_NAME, "inventory-error")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to(self):
        pass

    def add_product_to_cart(self, product_name):
        self.click_element(self.ADD_TO_CART_BUTTON_E)

    def is_product_visible(self, product_name):
        return self.is_element_visible(self.PRODUCT_D_CARD)

    def is_subscription_indicator_visible(self, product_name):
        subscription_locator = (By.XPATH, f"//span[@data-product='{product_name}'][@class='subscription']")
        return self.is_element_visible(subscription_locator)

    def validate_product_visible(self, product_name):
        return self.is_element_visible(self.PRODUCT_E_ROW)

    def validate_stock_info(self, product_name, expected_stock):
        stock_element = self.driver.find_element(*self.PRODUCT_E_STOCK_LABEL)
        actual_stock = stock_element.text
        return actual_stock == expected_stock

    def validate_inventory_error_displayed(self):
        return self.is_element_visible(self.INVENTORY_ERROR_MESSAGE)