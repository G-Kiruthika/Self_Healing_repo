from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ShoppingCartPage(BasePage):
    """Page Object for Shopping Cart functionality."""
    
    # Locators
    ADD_PRODUCT_A_BUTTON = (By.ID, "add-product-a-btn")
    ADD_PRODUCT_B_BUTTON = (By.ID, "add-product-b-btn")
    CART_ICON = (By.ID, "cart-icon")
    PRODUCT_ROW = (By.CLASS_NAME, "product-row")
    PRODUCT_A_QUANTITY_FIELD = (By.ID, "product-a-qty")
    PRODUCT_B_QUANTITY_FIELD = (By.ID, "product-b-qty")
    CART_TOTAL = (By.ID, "cart-total")
    LOADING_SPINNER = (By.ID, "loading-spinner")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def add_product_to_cart(self, product_name, quantity):
        """Adds a product to the cart with specified quantity.
        
        Args:
            product_name (str): Name of the product (e.g., 'Product A', 'Product B')
            quantity (int): Quantity to add
        """
        if product_name.lower() == 'product a':
            self.click_element(self.ADD_PRODUCT_A_BUTTON)
        elif product_name.lower() == 'product b':
            self.click_element(self.ADD_PRODUCT_B_BUTTON)
        else:
            raise ValueError(f"Unknown product: {product_name}")
        
        # Set quantity if needed
        if quantity > 1:
            self.change_product_quantity(product_name, quantity)
    
    def navigate_to_cart(self):
        """Navigates to the shopping cart by clicking the cart icon."""
        self.click_element(self.CART_ICON)
    
    def change_product_quantity(self, product_name, quantity):
        """Changes the quantity of a product in the cart.
        
        Args:
            product_name (str): Name of the product
            quantity (int): New quantity value
        """
        if product_name.lower() == 'product a':
            quantity_field = self.PRODUCT_A_QUANTITY_FIELD
        elif product_name.lower() == 'product b':
            quantity_field = self.PRODUCT_B_QUANTITY_FIELD
        else:
            raise ValueError(f"Unknown product: {product_name}")
        
        self.enter_text(quantity_field, str(quantity))
    
    def verify_product_in_cart(self, product_name, quantity, subtotal):
        """Verifies that a product is present in the cart with correct details.
        
        Args:
            product_name (str): Name of the product
            quantity (int): Expected quantity
            subtotal (float): Expected subtotal
            
        Returns:
            bool: True if product details match, False otherwise
        """
        try:
            # Locate product row and verify details
            product_rows = self.driver.find_elements(*self.PRODUCT_ROW)
            for row in product_rows:
                if product_name.lower() in row.text.lower():
                    # Verify quantity and subtotal in row text
                    if str(quantity) in row.text and str(subtotal) in row.text:
                        return True
            return False
        except Exception:
            return False
    
    def verify_cart_total(self, expected_total):
        """Verifies the cart total matches the expected value.
        
        Args:
            expected_total (float): Expected cart total
            
        Returns:
            bool: True if total matches, False otherwise
        """
        try:
            cart_total_element = self.driver.find_element(*self.CART_TOTAL)
            actual_total = cart_total_element.text.strip()
            return str(expected_total) in actual_total
        except Exception:
            return False
    
    def verify_no_loading_spinner(self):
        """Verifies that the loading spinner is not visible.
        
        Returns:
            bool: True if spinner is not visible, False if visible
        """
        return not self.is_element_visible(self.LOADING_SPINNER)
