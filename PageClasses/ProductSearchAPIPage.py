# ProductSearchAPIPage.py
"""
ProductSearchAPIPage
====================

Implements Page Object Model for product search API testing.
Covers TC-SCRUM-96-008: 
1. Send GET request to /api/products/search with 'laptop'
2. Validate HTTP 200 and products match search
3. Verify each product contains required fields

Author: Automation Orchestration Agent
Date: 2024-06-10
"""

import requests
from typing import List, Dict, Any

class ProductSearchAPIPage:
    """
    Page Object for the Product Search API.
    Provides methods to search for products and validate the response schema.
    """
    BASE_URL = "https://example-ecommerce.com"
    SEARCH_ENDPOINT = "/api/products/search"
    REQUIRED_PRODUCT_FIELDS = ["id", "name", "price", "description", "category", "imageUrl"]

    def __init__(self, base_url: str = None):
        """
        Optionally override the base URL (useful for different environments).
        """
        self.base_url = base_url or self.BASE_URL

    def search_products(self, keyword: str) -> requests.Response:
        """
        Sends a GET request to the search endpoint with the specified keyword.
        Args:
            keyword (str): Product search keyword (e.g., 'laptop')
        Returns:
            requests.Response: The API response object
        Raises:
            AssertionError: If the response status code is not 200
        """
        url = f"{self.base_url}{self.SEARCH_ENDPOINT}"
        params = {"q": keyword}
        response = requests.get(url, params=params)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
        return response

    def validate_products_match_search(self, response: requests.Response, keyword: str) -> List[Dict[str, Any]]:
        """
        Validates that all returned products match the search keyword in their name or description.
        Args:
            response (requests.Response): The API response object
            keyword (str): The search keyword
        Returns:
            List[Dict]: The list of product dicts
        Raises:
            AssertionError: If any product does not match the keyword
        """
        data = response.json()
        products = data.get("products", [])
        assert isinstance(products, list), f"'products' should be a list, got {type(products)}"
        for product in products:
            name = product.get("name", "").lower()
            description = product.get("description", "").lower()
            assert keyword.lower() in name or keyword.lower() in description, (
                f"Product {product.get('id', '<no id>')} does not match keyword '{keyword}'. Name: '{name}', Description: '{description}'"
            )
        return products

    def validate_product_schema(self, products: List[Dict[str, Any]]) -> None:
        """
        Validates that each product contains all required fields.
        Args:
            products (List[Dict]): The list of product dicts
        Raises:
            AssertionError: If any product is missing required fields
        """
        for idx, product in enumerate(products):
            missing_fields = [field for field in self.REQUIRED_PRODUCT_FIELDS if field not in product]
            assert not missing_fields, (
                f"Product at index {idx} (ID: {product.get('id', '<no id>')}) is missing fields: {missing_fields}"
            )

    def run_full_search_and_validation(self, keyword: str = "laptop") -> None:
        """
        Complete workflow for TC-SCRUM-96-008:
        1. Send GET request to search endpoint
        2. Validate HTTP 200
        3. Validate products match search keyword
        4. Validate product schema
        Raises:
            AssertionError: If any step fails
        """
        response = self.search_products(keyword)
        products = self.validate_products_match_search(response, keyword)
        self.validate_product_schema(products)

"""
Executive Summary
-----------------
- This Page Object automates the end-to-end validation of the Product Search API as per TC-SCRUM-96-008.
- It ensures HTTP status validation, keyword relevance, and strict schema compliance for all products.

Analysis
--------
- API endpoint: /api/products/search
- Query parameter: q (search keyword)
- Expected response: HTTP 200, JSON body with 'products' array. Each product must have id, name, price, description, category, imageUrl.

Implementation Guide
--------------------
1. Instantiate ProductSearchAPIPage.
2. Call run_full_search_and_validation() with desired keyword (default: 'laptop').
3. Use individual methods for granular validation if needed.

QA Report
---------
- All key validation steps are asserted.
- Failures raise clear AssertionError with diagnostic messages.
- Schema validation covers all required fields.

Troubleshooting
---------------
- If HTTP 200 is not returned, check API health and endpoint URL.
- If products are missing required fields, check backend API implementation.
- If keyword matching fails, review search logic or test data.

Future Considerations
---------------------
- Add support for authentication headers if required.
- Parameterize required fields and endpoint for different environments.
- Extend schema checks for nested structures or additional fields.
- Integrate with Locators.json if UI/API hybrid validation is needed.
"""
