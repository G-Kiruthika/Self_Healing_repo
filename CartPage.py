from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CartPage:
    """
    Page Object for Cart functionality.
    Implements methods for adding a product to cart, handling quantity input, and validating error messages.
    Strictly follows Selenium Python best practices for maintainability and downstream automation.

    Test Case: TC_CART_005
    - Attempt to add a product to cart with quantity greater than available stock.
    - Test Data: {"product_id": "12345", "quantity": 101}
    - Expected: System returns error; product not added.
    """
    # Locators (example IDs/classes, adjust as per actual app)
    PRODUCT_QUANTITY_INPUT = (By.ID, 'product-quantity')
    ADD_TO_CART_BUTTON = (By.ID, 'add-to-cart')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.error-message, .alert-danger, .cart-error')

    def __init__(self, driver, timeout=10):
        """
        Args:
            driver (WebDriver): Selenium WebDriver instance
            timeout (int): Default timeout for waits (seconds)
        """
        self.driver = driver
        self.timeout = timeout

    def set_quantity(self, quantity):
        """
        Enters the desired quantity for the product.
        Args:
            quantity (int): Quantity to set
        """
        qty_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PRODUCT_QUANTITY_INPUT)
        )
        qty_input.clear()
        qty_input.send_keys(str(quantity))

    def add_product_to_cart(self):
        """
        Clicks the 'Add to Cart' button.
        """
        add_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)
        )
        add_btn.click()

    def get_error_message(self):
        """
        Waits for and retrieves the error message displayed when adding fails.
        Returns:
            str: The error message text, or None if not found.
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.text.strip()
        except TimeoutException:
            return None

    def add_product_with_quantity_and_validate_error(self, product_id, quantity):
        """
        Composite method for TC_CART_005:
        - Navigates to product page (assumes caller handles navigation)
        - Sets quantity, adds to cart, and validates error message for excessive quantity.
        Args:
            product_id (str): Product identifier (assumes navigation done)
            quantity (int): Quantity to add
        Returns:
            str: Error message if present, else None
        Raises:
            AssertionError: If error message is not shown when expected
        """
        self.set_quantity(quantity)
        self.add_product_to_cart()
        error_msg = self.get_error_message()
        if not error_msg:
            raise AssertionError("Expected error message when adding quantity greater than stock, but none was shown.")
        return error_msg

"""
Executive Summary:
- CartPage.py implements atomic and composite actions for cart quantity validation (TC_CART_005).
- Methods: set_quantity, add_product_to_cart, get_error_message, add_product_with_quantity_and_validate_error.

Analysis:
- Enables robust automation for negative cart scenarios.

Implementation Guide:
1. Navigate to product page for product_id.
2. Call add_product_with_quantity_and_validate_error(product_id, quantity).
3. Validate error message matches expected.

QA Report:
- Strict Selenium best practices: explicit waits, error handling, docstrings.
- Imports validated.

Troubleshooting:
- If error not found, check locators and app state.
- Adjust timeout if needed for slow UI.

Future Considerations:
- Parameterize locators for multi-app support.
- Extend for positive cart flows and other error types.
"""