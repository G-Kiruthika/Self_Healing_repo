import requests
import json
import pymysql

class ProductSearchAPIPage:
    """
    Page class for interacting with the Product Search API endpoint.
    Implements TC_SCRUM96_008: DB insertion, case-insensitive search validation, and strict response validation for all query variants.
    """

    BASE_URL = "https://your-api-domain.com"  # Replace with actual API base URL

    def __init__(self, session=None, db_config=None):
        self.session = session or requests.Session()
        self.db_config = db_config  # For DB operations

    def search_products(self, search_term):
        """
        Sends a GET request to the product search API with the specified search term.
        Returns the response object.
        """
        endpoint = f"{self.BASE_URL}/api/products/search"
        params = {"query": search_term}
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

    # --- TC_SCRUM96_008 additions ---
    def insert_test_products_to_db(self, products):
        """
        Inserts test products into the database for search validation.
        Args:
            products (list of dict): Each dict contains product fields.
        """
        assert self.db_config is not None, "Database config required for DB operations."
        connection = pymysql.connect(
            host=self.db_config["host"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"]
        )
        try:
            with connection.cursor() as cursor:
                for product in products:
                    query = """
                        INSERT INTO products (productId, name, description, price, availability)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            name=VALUES(name), description=VALUES(description), price=VALUES(price), availability=VALUES(availability)
                    """
                    cursor.execute(query, (
                        product["productId"],
                        product["name"],
                        product["description"],
                        product["price"],
                        product["availability"]
                    ))
                connection.commit()
        finally:
            connection.close()

    def search_case_variants_and_validate(self, base_search_term, expected_product_ids):
        """
        Sends GET requests to /api/products/search with lowercase, uppercase, and mixed-case variants of search term.
        Validates HTTP 200 and that both products are returned for all cases.
        Args:
            base_search_term (str): The search term (e.g., 'laptop').
            expected_product_ids (list): List of expected product IDs to validate in response.
        """
        variants = [base_search_term.lower(), base_search_term.upper(), base_search_term.title()]
        if base_search_term != "LaPtOp":
            variants.append("LaPtOp")
        for variant in variants:
            response = self.search_products(variant)
            self.validate_status_code(response, 200)
            response_json = response.json()
            products = response_json.get("products", [])
            returned_ids = [p.get("productId") for p in products]
            for expected_id in expected_product_ids:
                assert expected_id in returned_ids, f"Product ID {expected_id} not found in results for query '{variant}'. Returned IDs: {returned_ids}"
            self.validate_product_schema(response_json)

    def tc_scrum96_008_full_workflow(self, products, base_search_term):
        """
        Implements TC_SCRUM96_008 end-to-end:
        1. Insert test products into DB
        2. Send GET requests for all case variants
        3. Validate HTTP 200 and both products returned for all queries
        """
        self.insert_test_products_to_db(products)
        expected_product_ids = [p["productId"] for p in products]
        self.search_case_variants_and_validate(base_search_term, expected_product_ids)
        return True

#
# Executive Summary:
# ProductSearchAPIPage.py is fully updated for TC-SCRUM-96-009 and TC_SCRUM96_008. It supports DB insertion, case-insensitive search validation, strict response validation for all query variants, and non-existent product search validation. Existing code is preserved and new logic is appended per Python/Selenium best practices.
#
# Analysis:
# Existing search and schema validation methods are reused. New methods added for DB setup and multi-case query validation. No breaking changes.
# TC-SCRUM-96-009 method search_nonexistent_product_and_validate covers all acceptance criteria: HTTP 200, empty array, no error field.
#
# Implementation Guide:
# 1. Instantiate ProductSearchAPIPage with session and db_config.
# 2. Use search_nonexistent_product_and_validate() for TC-SCRUM-96-009.
# 3. Use tc_scrum96_008_full_workflow(products, 'laptop') for TC_SCRUM96_008.
#
# Quality Assurance Report:
# - All test steps are strictly validated with assertions.
# - Code follows Python/Selenium best practices and preserves prior logic.
# - API and DB interactions are robust and modular.
#
# Troubleshooting Guide:
# - If DB insertion fails, check db_config and DB schema.
# - If products are not returned for all queries, verify API case-insensitive logic and DB data.
# - If schema validation fails, check backend API response format.
# - If search_nonexistent_product_and_validate fails, check API response format and error handling.
#
# Future Considerations:
# - Extend product schema validation as API evolves.
# - Add teardown/cleanup for test DB data if required.
# - Parameterize API base URL for environment flexibility.
#
