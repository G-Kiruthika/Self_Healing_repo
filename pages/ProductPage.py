# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.product_search_input = (By.ID, 'search-input')
        self.product_search_button = (By.CSS_SELECTOR, 'button.search-btn')
        self.product_list_item = (By.XPATH, "//div[@class='product-item' and @data-product-id='12345']")
        self.product_quantity_input = (By.CSS_SELECTOR, 'input.quantity-input')
        self.add_to_cart_button = (By.XPATH, "//button[contains(@class, 'add-to-cart') and ancestor::div[@data-product-id='12345']]")

    def search_product(self, product_id: str):
        search_input = self.driver.find_element(*self.product_search_input)
        search_input.clear()
        search_input.send_keys(product_id)
        self.driver.find_element(*self.product_search_button).click()

    def select_product(self):
        self.driver.find_element(*self.product_list_item).click()

    def set_quantity(self, quantity: int):
        quantity_input = self.driver.find_element(*self.product_quantity_input)
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

    def add_to_cart(self):
        self.driver.find_element(*self.add_to_cart_button).click()
