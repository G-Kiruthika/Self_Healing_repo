from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    SEARCH_BOX = (By.ID, "product_search")
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class, 'product-card')]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@class, 'add-to-cart')]")
    SUBSCRIPTION_OPTION = (By.XPATH, "//input[@type='checkbox' and @name='subscription']")
    MIN_THRESHOLD_INDICATOR = (By.XPATH, "//span[contains(@class, 'min-threshold')]")

    def __init__(self, driver):
        super().__init__(driver)

    def search_product(self, product_name):
        """
        Searches for a product by name.
        Args:
            product_name (str): Name of the product to search
        """
        self.enter_text(self.SEARCH_BOX, product_name)

    def add_to_cart(self, product_id, quantity):
        """
        Adds a product to cart with specified quantity.
        Args:
            product_id (str): Product ID
            quantity (int): Quantity to add
        """
        # Locate product by ID and add to cart
        product_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//button[contains(@class, 'add-to-cart')]")
        self.click_element(product_locator)

    def select_subscription(self, product_id):
        """
        Selects subscription option for a product.
        Args:
            product_id (str): Product ID
        """
        subscription_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//input[@type='checkbox' and @name='subscription']")
        self.click_element(subscription_locator)

    def is_product_visible(self, product_id):
        """
        Validates if a product is visible.
        Args:
            product_id (str): Product ID
        Returns:
            bool: True if product is visible, False otherwise
        """
        product_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']")
        return self.is_element_visible(product_locator)

    def has_min_threshold_indicator(self, product_id):
        """
        Validates if product has minimum threshold indicator.
        Args:
            product_id (str): Product ID
        Returns:
            bool: True if indicator is present, False otherwise
        """
        indicator_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//span[contains(@class, 'min-threshold')]")
        return self.is_element_visible(indicator_locator)
