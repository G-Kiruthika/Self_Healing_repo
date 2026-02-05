# CartPage.py
"""
PageClass for Shopping Cart operations (TC_CART_004)
Implements method to attempt creating a cart without authentication and validate unauthorized access error.
Strict code integrity, ready for downstream automation.
"""
import requests

class CartPage:
    """
    Page Object Model for Cart API operations.
    """
    CART_API_URL = "https://example-ecommerce.com/api/cart"

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
