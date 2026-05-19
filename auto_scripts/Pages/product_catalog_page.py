from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    PRODUCT_A_CARD = (By.XPATH, "//div[@data-product-name='Wireless Mouse']")
    PRODUCT_B_CARD = (By.XPATH, "//div[@data-product-name='Coffee Subscription']")
    ADD_TO_CART_A_BUTTON = (By.XPATH, "//div[@data-product-name='Wireless Mouse']//button[contains(text(),'Add to Cart')]")
    ADD_TO_CART_B_BUTTON = (By.XPATH, "//div[@data-product-name='Coffee Subscription']//button[contains(text(),'Add to Cart')]")

    def __init__(self, driver):
        super().__init__(driver)

    def add_product_to_cart(self, product_name):
        if product_name == "Wireless Mouse":
            self.click_element(self.ADD_TO_CART_A_BUTTON)
        elif product_name == "Coffee Subscription":
            self.click_element(self.ADD_TO_CART_B_BUTTON)
        else:
            raise ValueError(f"Product {product_name} not supported")

    def view_product(self, product_name):
        if product_name == "Wireless Mouse":
            self.click_element(self.PRODUCT_A_CARD)
        elif product_name == "Coffee Subscription":
            self.click_element(self.PRODUCT_B_CARD)
        else:
            raise ValueError(f"Product {product_name} not supported")

    def is_product_visible(self, product_name):
        if product_name == "Wireless Mouse":
            return self.is_element_visible(self.PRODUCT_A_CARD)
        elif product_name == "Coffee Subscription":
            return self.is_element_visible(self.PRODUCT_B_CARD)
        else:
            return False

    def is_minimum_threshold_displayed(self, product_name):
        threshold_locator = (By.XPATH, f"//div[@data-product-name='{product_name}']//span[@class='minimum-threshold']")
        return self.is_element_visible(threshold_locator)