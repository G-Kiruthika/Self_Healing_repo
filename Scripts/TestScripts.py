# TestScripts.py
"""
Automated Test Scripts for Product Search API
Covers TC_CART_003: Product search workflow validation
"""

import unittest
from PageClasses.ProductSearchAPIPage import ProductSearchAPIPage

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

if __name__ == "__main__":
    unittest.main()
