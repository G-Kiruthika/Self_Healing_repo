import requests
import json

class ProductSearchAPIPage:
    """
    Page class for interacting with the Product Search API endpoint.
    """

    BASE_URL = "https://your-api-domain.com"  # Replace with actual API base URL

    def __init__(self, session=None):
        self.session = session or requests.Session()

    def search_products(self, search_term):
        """
        Sends a GET request to the product search API with the specified search term.
        Returns the response object.
        """
        endpoint = f"{self.BASE_URL}/api/products/search"
        params = {"q": search_term}
        response = self.session.get(endpoint, params=params)
        return response

    def validate_status_code(self, response, expected_code=200):
        """
        Validates that the response status code matches the expected value.
        """
        assert response.status_code == expected_code, (
            f"Expected status code {expected_code}, got {response.status_code}"
        )

    def validate_products_contain_search_term(self, response_json, search_term):
        """
        Validates that each returned product contains the search term in its name or description.
        """
        products = response_json.get("products", [])
        for product in products:
            name = product.get("name", "").lower()
            description = product.get("description", "").lower()
            assert (
                search_term.lower() in name or search_term.lower() in description
            ), (
                f"Product {product.get('productId', 'N/A')} does not contain search term '{search_term}' in name or description."
            )

    def validate_product_schema(self, response_json):
        """
        Validates that each product contains the required fields: productId, name, description, price, availability.
        """
        required_fields = ["productId", "name", "description", "price", "availability"]
        products = response_json.get("products", [])
        for product in products:
            for field in required_fields:
                assert field in product, (
                    f"Product {product.get('productId', 'N/A')} is missing required field '{field}'."
                )

    def run_full_product_search_validation(self, search_term):
        """
        Executes the full validation workflow for the product search API.
        """
        response = self.search_products(search_term)
        self.validate_status_code(response, 200)
        response_json = response.json()
        self.validate_products_contain_search_term(response_json, search_term)
        self.validate_product_schema(response_json)

    # --- TC-SCRUM-96-009: Search with non-existent product ---
    def search_nonexistent_product_and_validate(self, nonexistent_search_term="nonexistentproduct12345"):
        """
        1. Send GET request to /api/products/search with a non-existent search term.
        2. Expect HTTP 200 and empty product list.
        3. Validate response structure with empty array {"products": []}.
        4. Ensure no error is thrown in the response for empty results.
        """
        response = self.search_products(nonexistent_search_term)
        self.validate_status_code(response, 200)
        try:
            response_json = response.json()
        except Exception as e:
            raise AssertionError(f"Response is not valid JSON: {e}")

        # Validate response structure is {"products": []}
        assert "products" in response_json, "Response JSON does not contain 'products' key."
        assert isinstance(response_json["products"], list), "'products' is not a list."
        assert len(response_json["products"]) == 0, f"Expected empty product list, got {len(response_json['products'])} items."

        # Ensure no error is present in the response for empty results
        assert "error" not in response_json, "Unexpected 'error' key in response for empty search result."
        assert response_json["products"] == [], "Expected 'products' to be an empty list."

# Example usage (for test automation pipeline):
# product_search_api = ProductSearchAPIPage()
# product_search_api.run_full_product_search_validation('laptop')
# product_search_api.search_nonexistent_product_and_validate()
