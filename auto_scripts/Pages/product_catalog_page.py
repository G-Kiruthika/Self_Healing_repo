from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    # Locators
    CATALOG_ROOT = (By.XPATH, "//div[@id='product-catalog']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to(self):
        """
        Navigates to the product catalog page.
        """
        self.driver.get("https://example-ecommerce.com/catalog")
        self.wait_for_element(self.CATALOG_ROOT)

    def is_catalog_displayed(self):
        """
        Validates if the product catalog is displayed.
        Returns:
            bool: True if catalog is displayed, False otherwise
        """
        return self.is_element_visible(self.CATALOG_ROOT)
