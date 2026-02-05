import pytest
from UserRegistrationAPIPage import UserRegistrationAPIPage
from ProfilePage import ProfilePage

class TestCartAPI:
    def test_TC_CART_001(self):
        """
        Test Case TC_CART_001:
        1. Register a new user via API.
        2. Authenticate with the new credentials and obtain JWT token.
        3. Simulate cart creation via API for the new user.
        4. Assert user account creation, authentication, token receipt, and cart association.
        """
        user_data = {
            "username": "newuser1",
            "email": "newuser1@example.com",
            "password": "StrongPass123",
            "firstName": "New",
            "lastName": "User"
        }
        # Register and authenticate user
        reg_api = UserRegistrationAPIPage()
        jwt_token = reg_api.register_user_and_get_jwt(user_data)
        assert jwt_token, "JWT token was not returned after registration and login."

        # Fetch user profile to get user_id
        profile_api = ProfilePage(None)
        profile_json = profile_api.fetch_profile_api(jwt_token)
        assert profile_json, "Profile fetch failed."
        user_id = profile_json.get("userId")
        assert user_id, "User ID not found in profile response."

        # Simulate cart creation via API (mocked, as Cart API PageClass not provided)
        import requests
        CART_API_URL = "https://example-ecommerce.com/api/cart/create"
        cart_payload = {"user_id": user_id}
        cart_headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
        try:
            cart_resp = requests.post(CART_API_URL, json=cart_payload, headers=cart_headers, timeout=10)
            cart_resp.raise_for_status()
            cart_json = cart_resp.json()
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Cart creation API failed: {e}")

        assert cart_json.get("cartId"), "Cart creation failed, cartId not present."
        assert cart_json.get("userId") == user_id, "Cart not associated with correct user."
        print("Test Case TC_CART_001 passed: User registered, authenticated, cart created.")

    def test_TC_CART_001_new(self):
        """
        Generated method for Test Case TC_CART_001 based on provided test steps:
        1. Navigate to the sign-up API endpoint and submit valid user details.
        2. Authenticate using the newly created credentials.
        3. Create a new shopping cart via API for the user.
        """
        user_data = {
            "username": "newuser1",
            "email": "newuser1@example.com",
            "password": "StrongPass123"
        }
        reg_api = UserRegistrationAPIPage()
        jwt_token = reg_api.register_user_and_get_jwt(user_data)
        assert jwt_token, "JWT token was not returned after registration and login."
        profile_api = ProfilePage(None)
        profile_json = profile_api.fetch_profile_api(jwt_token)
        assert profile_json, "Profile fetch failed."
        user_id = profile_json.get("userId")
        assert user_id, "User ID not found in profile response."
        import requests
        CART_API_URL = "https://example-ecommerce.com/api/cart/create"
        cart_payload = {"user_id": user_id}
        cart_headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
        cart_resp = requests.post(CART_API_URL, json=cart_payload, headers=cart_headers)
        assert cart_resp.status_code == 200, f"Cart creation failed: {cart_resp.text}"
        cart_json = cart_resp.json()
        assert cart_json.get("cartId"), "Cart creation failed, cartId not present."
        assert cart_json.get("userId") == user_id, "Cart not associated with correct user."
        print("Test Case TC_CART_001_new passed: User registered, authenticated, cart created.")
