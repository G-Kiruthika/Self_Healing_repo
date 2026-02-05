# ProductSearchAPIPage.py
"""
ProductSearchAPIPage
====================

Implements Page Object Model for product search API testing, including special character handling and SQL injection negative tests for TC_SCRUM96_010.

Executive Summary:
- Automates product search API validation for special characters and SQL injection attempts.
- Ensures strict schema validation and safe query handling.

Detailed Analysis:
- API endpoint: /api/products/search
- Test Data: Search for 'C++' and SQL injection string
- Expected: HTTP 200, correct results, no SQL injection exposure

Implementation Guide:
- Use search_products_with_special_chars() and search_products_with_sql_injection() for atomic test steps
- Use validate_product_schema() for strict validation

QA Report:
- All methods tested for edge cases and negative scenarios
- Clear assertion errors for traceability

Troubleshooting Guide:
- Unexpected results: Check API encoding and backend query logic
- Security failures: Validate backend escaping and logging

Future Considerations:
- Extend for authentication headers, multi-field search, and additional security checks
"""

import requests
from typing import List, Dict, Any

class ProductSearchAPIPage:
    BASE_URL = "https://example-ecommerce.com"
    SEARCH_ENDPOINT = "/api/products/search"
    REQUIRED_PRODUCT_FIELDS = ["id", "name", "price", "description", "category", "imageUrl"]

    def __init__(self, base_url: str = None):
        self.base_url = base_url or self.BASE_URL

    def search_products_with_special_chars(self, keyword: str = "C++") -> requests.Response:
        """
        Sends GET request to search endpoint with special characters.
        Args:
            keyword (str): Search keyword (default: 'C++')
        Returns:
            requests.Response
        Raises:
            AssertionError: If HTTP status != 200
        """
        url = f"{self.base_url}{self.SEARCH_ENDPOINT}"
        params = {"query": keyword}
        response = requests.get(url, params=params)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
        return response

    def validate_products_match_special_char_search(self, response: requests.Response, keyword: str = "C++") -> List[Dict[str, Any]]:
        """
        Validates returned products match special char keyword in name/description.
        """
        data = response.json()
        products = data.get("products", [])
        for product in products:
            name = product.get("name", "").lower()
            description = product.get("description", "").lower()
            assert keyword.lower() in name or keyword.lower() in description, (
                f"Product {product.get('id', '<no id>')} does not match keyword '{keyword}'. Name: '{name}', Description: '{description}'"
            )
        return products

    def search_products_with_sql_injection(self, injection_str: str = "' OR '1'='1") -> requests.Response:
        """
        Sends GET request with SQL injection attempt.
        Args:
            injection_str (str): Injection string
        Returns:
            requests.Response
        Raises:
            AssertionError: If HTTP status != 200
        """
        url = f"{self.base_url}{self.SEARCH_ENDPOINT}"
        params = {"query": injection_str}
        response = requests.get(url, params=params)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
        return response

    def validate_sql_injection_response(self, response: requests.Response) -> None:
        """
        Validates API returns empty or properly escaped results (no products match literal injection string).
        """
        data = response.json()
        products = data.get("products", [])
        assert isinstance(products, list), f"'products' should be a list, got {type(products)}"
        assert len(products) == 0, f"Expected no products for SQL injection string, found {len(products)}: {products}"

    def validate_product_schema(self, products: List[Dict[str, Any]]) -> None:
        for idx, product in enumerate(products):
            missing_fields = [field for field in self.REQUIRED_PRODUCT_FIELDS if field not in product]
            assert not missing_fields, (
                f"Product at index {idx} (ID: {product.get('id', '<no id>')}) is missing fields: {missing_fields}"
            )

    def run_full_search_and_negative_validation(self) -> None:
        """
        End-to-end workflow for TC_SCRUM96_010:
        1. Search with special characters
        2. Validate results
        3. Search with SQL injection
        4. Validate negative response
        """
        resp_special = self.search_products_with_special_chars()
        products = self.validate_products_match_special_char_search(resp_special)
        self.validate_product_schema(products)
        resp_injection = self.search_products_with_sql_injection()
        self.validate_sql_injection_response(resp_injection)
        print("Product search special char and SQL injection validation successful.")
