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

# Example usage (for test automation pipeline):
# product_search_api = ProductSearchAPIPage()
# product_search_api.run_full_product_search_validation('laptop')
