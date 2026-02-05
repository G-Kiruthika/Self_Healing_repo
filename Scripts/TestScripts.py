# TestScripts.py
"""
Automated Test Scripts for Product Search API
Covers TC_CART_003: Product search workflow validation
"""

import unittest
from PageClasses.ProductSearchAPIPage import ProductSearchAPIPage
from PageClasses.CartAPIPage import CartAPIPage

class TestProductSearchAPI(unittest.TestCase):
    def test_TC_CART_003_product_search_laptop(self):
        """
        TC_CART_003:
        1. Send a product search request with keyword 'laptop'.
        2. Validate HTTP 200.
        3. Validate system returns matching products.
        4. Validate product schema.
        """
        page = ProductSearchAPIPage()
        # Step 1: Send search request
        response = page.search_products('laptop')
        # Step 2: Validate HTTP 200 (done in search_products)
        # Step 3: Validate returned products match search
        products = page.validate_products_match_search(response, 'laptop')
        # Step 4: Validate product schema
        page.validate_product_schema(products)

    def test_TC_CART_005_add_product_quantity_exceeds_stock(self):
        """
        TC_CART_005:
        1. Attempt to add a product to cart with quantity greater than available stock.
           Test Data: { "product_id": "12345", "quantity": 101 }
        Expected: System returns error; product not added.
        """
        cart_page = CartAPIPage()
        product_id = "12345"
        quantity = 101
        # Step 1: Attempt to add product with excessive quantity
        response = cart_page.add_product_to_cart(product_id=product_id, quantity=quantity)
        # Validate system returns error response
        self.assertTrue(cart_page.is_add_to_cart_error(response),
                        msg="Expected error when adding quantity greater than stock, but did not receive one.")
        # Optionally, check cart contents to ensure product not added
        cart_contents = cart_page.get_cart_contents()
        self.assertFalse(cart_page.is_product_in_cart(cart_contents, product_id),
                         msg="Product was added to cart despite exceeding available stock.")

if __name__ == "__main__":
    unittest.main()
