from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class ShoppingCartPage(BasePage):
    """
    Page Object Model for Shopping Cart Page
    Contains locators and methods for shopping cart interactions
    """

    # Locators
    CART_PAGE_HEADER = (By.CSS_SELECTOR, "h1.cart-header")
    CART_ICON = (By.ID, "cart-icon")
    CART_ITEMS_CONTAINER = (By.CSS_SELECTOR, "div.cart-items")
    CART_ITEM_ROW = (By.CSS_SELECTOR, "div.cart-item")
    CART_TOTAL = (By.ID, "cart-total")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "p.empty-cart-message")
    RETURN_TO_CATALOG_BUTTON = (By.ID, "return-to-catalog-btn")
    LOADING_SPINNER = (By.CSS_SELECTOR, "div.loading-spinner")
    
    # Dynamic locators (require formatting with product name)
    PRODUCT_NAME = (By.XPATH, "//div[@class='cart-item']//span[@class='product-name' and text()='{}']")
    PRODUCT_UNIT_PRICE = (By.XPATH, "//div[@class='cart-item']//span[@class='product-name' and text()='{}']/ancestor::div[@class='cart-item']//span[@class='unit-price']")
    PRODUCT_QUANTITY_INPUT = (By.XPATH, "//div[@class='cart-item']//span[@class='product-name' and text()='{}']/ancestor::div[@class='cart-item']//input[@class='quantity-input']")
    PRODUCT_SUBTOTAL = (By.XPATH, "//div[@class='cart-item']//span[@class='product-name' and text()='{}']/ancestor::div[@class='cart-item']//span[@class='subtotal']")
    PRODUCT_DELETE_BUTTON = (By.XPATH, "//div[@class='cart-item']//span[@class='product-name' and text()='{}']/ancestor::div[@class='cart-item']//button[@class='delete-btn']")

    def __init__(self, driver):
        """Initialize ShoppingCartPage with driver"""
        super().__init__(driver)
        self.url = "https://example.com/cart"  # Update with actual cart URL

    def open(self):
        """Navigate to shopping cart page"""
        self.driver.get(self.url)
        self.wait_for_page_load()

    def navigate_to_cart(self):
        """Navigate to cart by clicking cart icon"""
        self.click_element(self.CART_ICON)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for cart page to load completely"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_ITEMS_CONTAINER)
        )

    def is_cart_page_displayed(self):
        """Check if shopping cart page is displayed"""
        return self.is_element_visible(self.CART_PAGE_HEADER)

    def is_product_in_cart(self, product_name):
        """Check if a specific product is present in cart"""
        locator = (self.PRODUCT_NAME[0], self.PRODUCT_NAME[1].format(product_name))
        return self.is_element_visible(locator)

    def get_product_name(self, product_name):
        """Get product name from cart"""
        locator = (self.PRODUCT_NAME[0], self.PRODUCT_NAME[1].format(product_name))
        return self.get_element_text(locator)

    def get_product_unit_price(self, product_name):
        """Get unit price of a product"""
        locator = (self.PRODUCT_UNIT_PRICE[0], self.PRODUCT_UNIT_PRICE[1].format(product_name))
        return self.get_element_text(locator)

    def get_product_quantity(self, product_name):
        """Get quantity of a product"""
        locator = (self.PRODUCT_QUANTITY_INPUT[0], self.PRODUCT_QUANTITY_INPUT[1].format(product_name))
        element = self.find_element(locator)
        return element.get_attribute("value")

    def get_product_subtotal(self, product_name):
        """Get subtotal of a product"""
        locator = (self.PRODUCT_SUBTOTAL[0], self.PRODUCT_SUBTOTAL[1].format(product_name))
        return self.get_element_text(locator)

    def get_cart_total(self):
        """Get overall cart total"""
        return self.get_element_text(self.CART_TOTAL)

    def update_product_quantity(self, product_name, new_quantity):
        """Update quantity of a product in cart"""
        locator = (self.PRODUCT_QUANTITY_INPUT[0], self.PRODUCT_QUANTITY_INPUT[1].format(product_name))
        element = self.find_element(locator)
        element.clear()
        self.enter_text(locator, str(new_quantity))
        # Wait for update to process
        time.sleep(1)

    def remove_product_from_cart(self, product_name):
        """Remove a product from cart by clicking delete button"""
        locator = (self.PRODUCT_DELETE_BUTTON[0], self.PRODUCT_DELETE_BUTTON[1].format(product_name))
        self.click_element(locator)
        # Wait for removal to process
        time.sleep(1)

    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)

    def get_empty_cart_message(self):
        """Get empty cart message text"""
        return self.get_element_text(self.EMPTY_CART_MESSAGE)

    def is_return_to_catalog_button_visible(self):
        """Check if 'Return to Product Catalog' button is visible"""
        return self.is_element_visible(self.RETURN_TO_CATALOG_BUTTON)

    def get_cart_item_count(self):
        """Get count of items in cart"""
        try:
            elements = self.driver.find_elements(*self.CART_ITEM_ROW)
            return len(elements)
        except:
            return 0

    def is_loading_spinner_visible(self):
        """Check if loading spinner is visible"""
        try:
            return self.is_element_visible(self.LOADING_SPINNER)
        except:
            return False

    def is_page_refreshed(self):
        """Check if page was refreshed by monitoring page load state"""
        # Store current page state
        try:
            initial_element = self.find_element(self.CART_PAGE_HEADER)
            time.sleep(0.5)
            current_element = self.find_element(self.CART_PAGE_HEADER)
            # If elements are different objects, page was refreshed
            return initial_element != current_element
        except:
            return False