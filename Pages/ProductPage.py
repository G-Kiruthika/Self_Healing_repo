# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.product_search_input = (By.ID, 'search-input')
        self.product_search_button = (By.CSS_SELECTOR, 'button.search-btn')
        self.product_quantity_input = (By.CSS_SELECTOR, 'input.quantity-input')
        self.add_to_cart_button_tpl = (By.XPATH, "//button[contains(@class, 'add-to-cart') and ancestor::div[@data-product-id='{}']]")
        self.product_list_item_tpl = (By.XPATH, "//div[@class='product-item' and @data-product-id='{}']")
        self.product_error_message = (By.CSS_SELECTOR, '.product-error-message')  # Placeholder for error message

    def search_product(self, product_id: str):
        search_input = self.driver.find_element(*self.product_search_input)
        search_input.clear()
        search_input.send_keys(product_id)
        self.driver.find_element(*self.product_search_button).click()

    def select_product(self, product_id: str):
        """
        Attempts to select product by product_id. Returns True if found, False if not found.
        """
        try:
            locator = (self.product_list_item_tpl[0], self.product_list_item_tpl[1].format(product_id))
            self.driver.find_element(*locator).click()
            return True
        except NoSuchElementException:
            return False

    def set_quantity(self, quantity: int):
        quantity_input = self.driver.find_element(*self.product_quantity_input)
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

    def add_to_cart(self, product_id: str):
        """
        Attempts to add product to cart by product_id. Returns True if button found and clicked, False otherwise.
        """
        try:
            add_btn_locator = (self.add_to_cart_button_tpl[0], self.add_to_cart_button_tpl[1].format(product_id))
            self.driver.find_element(*add_btn_locator).click()
            return True
        except NoSuchElementException:
            return False

    def get_error_message(self):
        """
        Returns error message displayed on product page, if any.
        """
        try:
            return self.driver.find_element(*self.product_error_message).text
        except NoSuchElementException:
            return None
