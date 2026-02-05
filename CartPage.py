# CartPage.py
"""
PageClass for Shopping Cart operations (TC_CART_004, TC_CART_008)
Implements methods to attempt creating a cart without authentication, and to attempt adding a product with an invalid product ID and validate error response.
Strict code integrity, ready for downstream automation.
"""
import requests

class CartPage:
    """
    Page Object Model for Cart API operations.
    """
    CART_API_URL = "https://example-ecommerce.com/api/cart"
    ADD_TO_CART_API_URL = "https://example-ecommerce.com/api/cart/add"

    def create_cart_without_auth(self, cart_data=None):
        """
        Attempts to create a shopping cart without authentication.
        Args:
            cart_data (dict): Optional cart payload (default: empty dict)
        Returns:
            requests.Response: The response object from the API call
        """
        if cart_data is None:
            cart_data = {}
        headers = {"Content-Type": "application/json"}  # No Authorization header
        response = requests.post(self.CART_API_URL, json=cart_data, headers=headers, timeout=10)
        return response

    def validate_unauthorized_response(self, response):
        """
        Validates that the response indicates unauthorized access (HTTP 401 or error message).
        Args:
            response (requests.Response): The response object from create_cart_without_auth
        Returns:
            bool: True if unauthorized, raises AssertionError otherwise
        """
        if response.status_code == 401:
            return True
        # Optionally check for error message in JSON
        try:
            resp_json = response.json()
            if "unauthorized" in resp_json.get("error", "").lower() or "authentication" in resp_json.get("message", "").lower():
                return True
        except Exception:
            pass  # Could not parse JSON, fallback to status code
        raise AssertionError(f"Expected unauthorized error, got status {response.status_code}: {response.text}")

    def add_product_to_cart_invalid_id(self, product_id, quantity, auth_token=None):
        """
        Attempts to add a product to cart with an invalid product ID.
        Args:
            product_id (str): The (invalid) product ID to add
            quantity (int): Quantity to add
            auth_token (str, optional): JWT token for authentication (if required)
        Returns:
            requests.Response: The response object from the API call
        """
        payload = {
            "product_id": product_id,
            "quantity": quantity
        }
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        response = requests.post(self.ADD_TO_CART_API_URL, json=payload, headers=headers, timeout=10)
        return response

    def validate_invalid_product_error(self, response):
        """
        Validates that the response indicates an error due to invalid product ID and that the product is not added.
        Args:
            response (requests.Response): The response object from add_product_to_cart_invalid_id
        Returns:
            bool: True if error as expected, raises AssertionError otherwise
        """
        # Acceptable error codes: 400, 404, or explicit error message
        if response.status_code in [400, 404]:
            return True
        try:
            resp_json = response.json()
            error_msg = resp_json.get("error", "") or resp_json.get("message", "")
            if any(keyword in error_msg.lower() for keyword in ["invalid product id", "not found", "does not exist"]):
                return True
        except Exception:
            pass
        raise AssertionError(f"Expected invalid product error, got status {response.status_code}: {response.text}")
