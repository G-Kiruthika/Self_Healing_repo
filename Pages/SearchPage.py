from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchPage:
    """
    Page class for product search functionality.
    """

    # Placeholder locators for search functionality
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search-btn")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".product-list")
    PRODUCT_ITEM = (By.CSS_SELECTOR, ".product-item")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search_product(self, keyword: str):
        """
        Sends a product search request using the provided keyword.

        Args:
            keyword (str): The search keyword.
        """
        # Wait for search input to be present and enter keyword
        search_input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(keyword)

        # Click the search button
        search_button = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        search_button.click()

    def validate_search_results(self, expected_keyword: str) -> bool:
        """
        Validates that matching products are returned after search.

        Args:
            expected_keyword (str): The keyword to validate in product results.

        Returns:
            bool: True if at least one matching product is found, False otherwise.
        """
        # Wait for product list to be visible
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_LIST))
        product_items = self.driver.find_elements(*self.PRODUCT_ITEM)

        for item in product_items:
            title_element = item.find_element(*self.PRODUCT_TITLE)
            if expected_keyword.lower() in title_element.text.lower():
                return True
        return False