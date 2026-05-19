from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    # Locators
    OUT_OF_STOCK_INDICATOR = (By.XPATH, "//span[contains(text(),'Out of Stock')]")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-btn")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    CART_ICON = (By.ID, "cart-icon")

    def __init__(self, driver):
        super().__init__(driver)

    def view_product(self, product_id):
        """
        Navigates to the product page for the given product ID.
        Args:
            product_id (str): Product ID to view
        """
        product_url = f"https://example-ecommerce.com/product/{product_id}"
        self.driver.get(product_url)
        self.wait_for_page_load()

    def click_add_to_cart(self):
        """
        Clicks the Add to Cart button.
        """
        self.click_element(self.ADD_TO_CART_BUTTON)

    def is_out_of_stock_displayed(self):
        """
        Validates if the out of stock indicator is displayed.
        Returns:
            bool: True if out of stock indicator is visible, False otherwise
        """
        return self.is_element_visible(self.OUT_OF_STOCK_INDICATOR)

    def is_add_to_cart_disabled(self):
        """
        Validates if the Add to Cart button is disabled.
        Returns:
            bool: True if button is disabled, False otherwise
        """
        try:
            button = self.driver.find_element(*self.ADD_TO_CART_BUTTON)
            return not button.is_enabled() or button.get_attribute("disabled") is not None
        except Exception:
            return False

    def is_error_message_displayed(self):
        """
        Validates if an error message is displayed.
        Returns:
            bool: True if error message is visible, False otherwise
        """
        return self.is_element_visible(self.ERROR_MESSAGE)

    def is_cart_unchanged(self):
        """
        Validates if the cart icon shows no change (no item count increase).
        Returns:
            bool: True if cart is unchanged, False otherwise
        """
        try:
            cart_icon = self.driver.find_element(*self.CART_ICON)
            cart_count = cart_icon.get_attribute("data-count") or "0"
            return cart_count == "0"
        except Exception:
            return True
