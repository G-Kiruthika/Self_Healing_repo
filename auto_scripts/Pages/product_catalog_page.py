from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    ADD_TO_CART_BUTTON_TD_01 = (By.XPATH, "//button[@data-sku='TD-01' and contains(text(),'Add to Cart')]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_product_catalog(self):
        """
        Navigates to the product catalog page.
        """
        self.driver.get("https://example-ecommerce.com/catalog")
        self.wait_for_page_load()

    def add_to_cart(self, sku):
        """
        Adds a product to cart by SKU.
        Args:
            sku (str): Product SKU
        """
        add_to_cart_locator = (By.XPATH, f"//button[@data-sku='{sku}' and contains(text(),'Add to Cart')]")
        self.click_element(add_to_cart_locator)
