from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    PRODUCT_D_CARD = (By.XPATH, "//div[@data-product='Vitamin Pack']")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[@data-product='Vitamin Pack'][text()='Add to Cart']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to(self):
        # Navigate to product catalog page
        pass

    def add_product_to_cart(self, product_name, quantity):
        # Add product to cart with specified quantity
        self.click_element(self.ADD_TO_CART_BUTTON)

    def is_product_visible(self, product_name):
        return self.is_element_visible(self.PRODUCT_D_CARD)

    def is_subscription_indicator_visible(self, product_name):
        subscription_locator = (By.XPATH, f"//span[@data-product='{product_name}'][@class='subscription']")
        return self.is_element_visible(subscription_locator)