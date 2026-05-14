from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductCatalogPage(BasePage):
    """
    Page Object Model for Product Catalog Page
    Contains locators and methods for product catalog interactions
    """

    # Locators
    CATALOG_HEADER = (By.CSS_SELECTOR, "h1.catalog-header")
    PRODUCT_GRID = (By.CSS_SELECTOR, "div.product-grid")
    CART_ICON = (By.ID, "cart-icon")
    
    # Dynamic locators (require formatting with product name)
    PRODUCT_CARD = (By.XPATH, "//div[@class='product-card']//h3[text()='{}']")
    PRODUCT_ADD_TO_CART_BUTTON = (By.XPATH, "//div[@class='product-card']//h3[text()='{}']/ancestor::div[@class='product-card']//button[@class='add-to-cart-btn']")
    PRODUCT_QUANTITY_INPUT = (By.XPATH, "//div[@class='product-card']//h3[text()='{}']/ancestor::div[@class='product-card']//input[@class='quantity-input']")
    PRODUCT_PRICE = (By.XPATH, "//div[@class='product-card']//h3[text()='{}']/ancestor::div[@class='product-card']//span[@class='price']")

    def __init__(self, driver):
        """Initialize ProductCatalogPage with driver"""
        super().__init__(driver)
        self.url = "https://example.com/catalog"  # Update with actual catalog URL

    def open(self):
        """Navigate to product catalog page"""
        self.driver.get(self.url)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for catalog page to load completely"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PRODUCT_GRID)
        )

    def is_catalog_page_displayed(self):
        """Check if product catalog page is displayed"""
        return self.is_element_visible(self.CATALOG_HEADER)

    def is_product_available(self, product_name):
        """Check if a specific product is available in catalog"""
        locator = (self.PRODUCT_CARD[0], self.PRODUCT_CARD[1].format(product_name))
        return self.is_element_visible(locator)

    def get_product_price(self, product_name):
        """Get price of a product"""
        locator = (self.PRODUCT_PRICE[0], self.PRODUCT_PRICE[1].format(product_name))
        return self.get_element_text(locator)

    def set_product_quantity(self, product_name, quantity):
        """Set quantity for a product before adding to cart"""
        locator = (self.PRODUCT_QUANTITY_INPUT[0], self.PRODUCT_QUANTITY_INPUT[1].format(product_name))
        if self.is_element_visible(locator):
            element = self.find_element(locator)
            element.clear()
            self.enter_text(locator, str(quantity))

    def click_add_to_cart(self, product_name):
        """Click add to cart button for a specific product"""
        locator = (self.PRODUCT_ADD_TO_CART_BUTTON[0], self.PRODUCT_ADD_TO_CART_BUTTON[1].format(product_name))
        self.click_element(locator)

    def add_product_to_cart(self, product_name, quantity=1):
        """Add a product to cart with specified quantity"""
        # Set quantity if input field exists
        self.set_product_quantity(product_name, quantity)
        # Click add to cart button
        self.click_add_to_cart(product_name)
        # Wait for action to complete
        WebDriverWait(self.driver, 5).until(
            lambda driver: True  # Add specific wait condition if needed
        )

    def navigate_to_cart(self):
        """Navigate to cart by clicking cart icon"""
        self.click_element(self.CART_ICON)