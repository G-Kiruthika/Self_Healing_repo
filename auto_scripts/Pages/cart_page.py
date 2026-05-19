from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEM = (By.XPATH, "//div[contains(@class, 'cart-item')]")
    PRODUCT_NAME = (By.XPATH, "//span[contains(@class, 'product-name')]")
    UNIT_PRICE = (By.XPATH, "//span[contains(@class, 'unit-price')]")
    QUANTITY = (By.XPATH, "//input[contains(@class, 'quantity-input')]")
    SUBTOTAL = (By.XPATH, "//span[contains(@class, 'subtotal')]")
    MIN_THRESHOLD_INDICATOR = (By.XPATH, "//span[contains(@class, 'min-threshold')]")
    SUBSCRIPTION_BADGE = (By.XPATH, "//span[contains(@class, 'subscription-badge')]")
    DELIVERY_FREQUENCY_OPTION = (By.XPATH, "//select[contains(@class, 'delivery-frequency')]")

    def __init__(self, driver):
        super().__init__(driver)

    def view_cart(self):
        """
        Navigates to cart page or refreshes cart view.
        """
        # Navigate to cart page
        self.driver.get("https://example-ecommerce.com/cart")

    def cart_contains_product(self, product_id, quantity):
        """
        Validates if cart contains a specific product with given quantity.
        Args:
            product_id (str): Product ID
            quantity (int): Expected quantity
        Returns:
            bool: True if product with quantity exists, False otherwise
        """
        product_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']")
        if not self.is_element_visible(product_locator):
            return False
        quantity_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//input[contains(@class, 'quantity-input')]")
        quantity_element = self.driver.find_element(*quantity_locator)
        actual_quantity = int(quantity_element.get_attribute('value'))
        return actual_quantity == quantity

    def cart_shows_min_threshold(self, product_id):
        """
        Validates if cart shows minimum threshold indicator for a product.
        Args:
            product_id (str): Product ID
        Returns:
            bool: True if indicator is visible, False otherwise
        """
        indicator_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//span[contains(@class, 'min-threshold')]")
        return self.is_element_visible(indicator_locator)

    def cart_shows_subscription_badge(self, product_id):
        """
        Validates if cart shows subscription badge for a product.
        Args:
            product_id (str): Product ID
        Returns:
            bool: True if badge is visible, False otherwise
        """
        badge_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//span[contains(@class, 'subscription-badge')]")
        return self.is_element_visible(badge_locator)

    def cart_shows_delivery_frequency(self, product_id):
        """
        Validates if cart shows delivery frequency option for a product.
        Args:
            product_id (str): Product ID
        Returns:
            bool: True if option is visible, False otherwise
        """
        frequency_locator = (By.XPATH, f"//div[@data-product-id='{product_id}']//select[contains(@class, 'delivery-frequency')]")
        return self.is_element_visible(frequency_locator)
