import pytest
from pages.shopping_cart_page import ShoppingCartPage
from pages.product_catalog_page import ProductCatalogPage
from core.driver_factory import get_driver
from utils.send_email_report import send_report


class TestShoppingCart:
    """Test suite for shopping cart functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method to initialize driver and page objects"""
        self.driver = get_driver()
        self.cart_page = ShoppingCartPage(self.driver)
        self.catalog_page = ProductCatalogPage(self.driver)
        yield
        self.driver.quit()

    def test_tc_004_verify_multiple_products_in_cart(self):
        """
        Test Case ID: TC-004
        Description: Verify multiple products are displayed correctly in shopping cart
        Steps:
        1. Add Product A (qty: 1) and Product B (qty: 3) to the cart
        2. Navigate to the shopping cart page
        3. Verify product details for Product A and Product B
        4. Check the overall cart total
        """
        try:
            # Step 1: Add Product A (qty: 1) and Product B (qty: 3) to the cart
            self.catalog_page.open()
            self.catalog_page.add_product_to_cart("Wireless Mouse", 1)
            self.catalog_page.add_product_to_cart("Coffee Subscription", 3)
            
            # Step 2: Navigate to the shopping cart page
            self.cart_page.navigate_to_cart()
            
            # Verify shopping cart page is displayed
            assert self.cart_page.is_cart_page_displayed(), "Shopping cart page is not displayed"
            
            # Step 3: Verify both products are present in the cart
            assert self.cart_page.is_product_in_cart("Wireless Mouse"), "Product A is not present in cart"
            assert self.cart_page.is_product_in_cart("Coffee Subscription"), "Product B is not present in cart"
            
            # Step 4: Verify product details for Product A
            product_a_name = self.cart_page.get_product_name("Wireless Mouse")
            product_a_price = self.cart_page.get_product_unit_price("Wireless Mouse")
            product_a_quantity = self.cart_page.get_product_quantity("Wireless Mouse")
            product_a_subtotal = self.cart_page.get_product_subtotal("Wireless Mouse")
            
            assert product_a_name == "Wireless Mouse", f"Expected 'Wireless Mouse', got '{product_a_name}'"
            assert product_a_price == "$25.00", f"Expected '$25.00', got '{product_a_price}'"
            assert product_a_quantity == "1", f"Expected quantity '1', got '{product_a_quantity}'"
            assert product_a_subtotal == "$25.00", f"Expected subtotal '$25.00', got '{product_a_subtotal}'"
            
            # Verify product details for Product B
            product_b_name = self.cart_page.get_product_name("Coffee Subscription")
            product_b_price = self.cart_page.get_product_unit_price("Coffee Subscription")
            product_b_quantity = self.cart_page.get_product_quantity("Coffee Subscription")
            product_b_subtotal = self.cart_page.get_product_subtotal("Coffee Subscription")
            
            assert product_b_name == "Coffee Subscription", f"Expected 'Coffee Subscription', got '{product_b_name}'"
            assert product_b_price == "$15.99", f"Expected '$15.99', got '{product_b_price}'"
            assert product_b_quantity == "3", f"Expected quantity '3', got '{product_b_quantity}'"
            assert product_b_subtotal == "$47.97", f"Expected subtotal '$47.97', got '{product_b_subtotal}'"
            
            # Step 5: Check the overall cart total
            cart_total = self.cart_page.get_cart_total()
            assert cart_total == "$72.97", f"Expected cart total '$72.97', got '{cart_total}'"
            
        except Exception as e:
            send_report(f"TC-004 failed: {str(e)}")
            raise

    def test_tc_005_verify_quantity_update_recalculation(self):
        """
        Test Case ID: TC-005
        Description: Verify cart totals update instantly when product quantity is changed
        Steps:
        1. Ensure Product A is in cart with quantity 1 and subtotal $25.00
        2. Change the quantity of Product A to 5
        3. Observe the line item subtotal and cart total
        4. Check for page refresh or loading spinner
        """
        try:
            # Step 1: Ensure Product A is in cart with quantity 1
            self.catalog_page.open()
            self.catalog_page.add_product_to_cart("Wireless Mouse", 1)
            self.cart_page.navigate_to_cart()
            
            # Verify Product A is present in cart
            assert self.cart_page.is_product_in_cart("Wireless Mouse"), "Product A is not present in cart"
            
            # Verify initial quantity and subtotal
            initial_quantity = self.cart_page.get_product_quantity("Wireless Mouse")
            initial_subtotal = self.cart_page.get_product_subtotal("Wireless Mouse")
            assert initial_quantity == "1", f"Expected initial quantity '1', got '{initial_quantity}'"
            assert initial_subtotal == "$25.00", f"Expected initial subtotal '$25.00', got '{initial_subtotal}'"
            
            # Step 2: Change the quantity of Product A to 5
            self.cart_page.update_product_quantity("Wireless Mouse", 5)
            
            # Step 3: Verify quantity updates to 5
            updated_quantity = self.cart_page.get_product_quantity("Wireless Mouse")
            assert updated_quantity == "5", f"Expected quantity '5', got '{updated_quantity}'"
            
            # Observe the line item subtotal and cart total
            updated_subtotal = self.cart_page.get_product_subtotal("Wireless Mouse")
            assert updated_subtotal == "$125.00", f"Expected line item subtotal '$125.00', got '{updated_subtotal}'"
            
            updated_cart_total = self.cart_page.get_cart_total()
            assert updated_cart_total == "$125.00", f"Expected cart total '$125.00', got '{updated_cart_total}'"
            
            # Step 4: Check for page refresh or loading spinner
            assert not self.cart_page.is_page_refreshed(), "Page refresh occurred unexpectedly"
            assert not self.cart_page.is_loading_spinner_visible(), "Loading spinner is visible"
            
        except Exception as e:
            send_report(f"TC-005 failed: {str(e)}")
            raise

    def test_tc_007_verify_product_removal_and_total_recalculation(self):
        """
        Test Case ID: TC-007
        Description: Verify product removal from cart and total recalculation
        Steps:
        1. Ensure Product A (subtotal $25.00) and Product C (subtotal $89.99) are in cart
        2. Click 'Delete' for Product C
        3. Check the cart total
        4. Verify only Product A remains in the cart
        """
        try:
            # Step 1: Ensure Product A and Product C are in cart
            self.catalog_page.open()
            self.catalog_page.add_product_to_cart("Wireless Mouse", 1)
            self.catalog_page.add_product_to_cart("Product C", 1)
            self.cart_page.navigate_to_cart()
            
            # Verify both products are present in cart
            assert self.cart_page.is_product_in_cart("Wireless Mouse"), "Product A is not present in cart"
            assert self.cart_page.is_product_in_cart("Product C"), "Product C is not present in cart"
            
            # Verify initial subtotals
            product_a_subtotal = self.cart_page.get_product_subtotal("Wireless Mouse")
            product_c_subtotal = self.cart_page.get_product_subtotal("Product C")
            assert product_a_subtotal == "$25.00", f"Expected Product A subtotal '$25.00', got '{product_a_subtotal}'"
            assert product_c_subtotal == "$89.99", f"Expected Product C subtotal '$89.99', got '{product_c_subtotal}'"
            
            # Step 2: Click 'Delete' for Product C
            self.cart_page.remove_product_from_cart("Product C")
            
            # Step 3: Verify Product C is removed from the cart
            assert not self.cart_page.is_product_in_cart("Product C"), "Product C is still present in cart"
            
            # Step 4: Check the cart total
            updated_cart_total = self.cart_page.get_cart_total()
            assert updated_cart_total == "$25.00", f"Expected cart total '$25.00', got '{updated_cart_total}'"
            
            # Step 5: Verify only Product A remains in the cart
            assert self.cart_page.is_product_in_cart("Wireless Mouse"), "Product A is not present in cart"
            product_count = self.cart_page.get_cart_item_count()
            assert product_count == 1, f"Expected 1 product in cart, got {product_count}"
            
        except Exception as e:
            send_report(f"TC-007 failed: {str(e)}")
            raise

    def test_tc_008_verify_empty_cart_display(self):
        """
        Test Case ID: TC-008
        Description: Verify empty cart displays appropriate message and call-to-action
        Steps:
        1. Ensure the shopping cart is empty
        2. Navigate to the cart page
        3. Observe the cart page
        """
        try:
            # Step 1: Ensure the shopping cart is empty
            self.cart_page.navigate_to_cart()
            
            # Step 2: Verify cart page is displayed
            assert self.cart_page.is_cart_page_displayed(), "Cart page is not displayed"
            
            # Step 3: Verify no items are present in the cart
            assert self.cart_page.is_cart_empty(), "Cart is not empty"
            
            # Step 4: Observe the cart page
            # Verify message 'Your cart is empty' is displayed
            empty_message = self.cart_page.get_empty_cart_message()
            assert empty_message == "Your cart is empty", f"Expected 'Your cart is empty', got '{empty_message}'"
            
            # Verify 'Return to Product Catalog' button is displayed
            assert self.cart_page.is_return_to_catalog_button_visible(), "'Return to Product Catalog' button is not visible"
            
            # Verify no product line items are shown
            product_count = self.cart_page.get_cart_item_count()
            assert product_count == 0, f"Expected 0 products in cart, got {product_count}"
            
        except Exception as e:
            send_report(f"TC-008 failed: {str(e)}")
            raise