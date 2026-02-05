import pytest
from UserRegistrationAPIPage import UserRegistrationAPIPage
from ProfilePage import ProfilePage

@pytest.mark.asyncio
async def test_cart_001():
    """
    Test Case TC_CART_001
    Steps:
    1. Register a new user via API
    2. Authenticate and retrieve JWT token
    3. Create a new shopping cart via API
    4. Validate account creation and cart association
    """
    # Step 1: Register new user
    user_data = {
        "username": "newuser1",
        "email": "newuser1@example.com",
        "password": "StrongPass123",
        "firstName": "New",
        "lastName": "User"
    }
    reg_api = UserRegistrationAPIPage()
    jwt_token = reg_api.register_user_and_get_jwt(user_data)
    assert jwt_token, "JWT token not received after registration/login"

    # Step 2: Fetch profile and validate
    profile_api = ProfilePage(None)
    profile_data = profile_api.fetch_profile_api(jwt_token)
    expected_data = {
        "username": "newuser1",
        "email": "newuser1@example.com",
        "firstName": "New",
        "lastName": "User"
    }
    assert profile_api.validate_profile_fields(profile_data, expected_data)

    # Step 3: Create cart via API
    import requests
    CART_API_URL = "https://example-ecommerce.com/api/cart/create"
    cart_payload = {"user_id": profile_data["userId"]}
    cart_headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
    cart_resp = requests.post(CART_API_URL, json=cart_payload, headers=cart_headers, timeout=10)
    assert cart_resp.status_code in [200, 201], f"Cart creation failed: {cart_resp.text}"
    cart_json = cart_resp.json()
    assert cart_json.get("cartId"), "Cart ID not returned after creation"
    assert cart_json.get("userId") == profile_data["userId"], "Cart not associated with correct user"
    print("TC_CART_001 passed: User registration, authentication, and cart creation validated.")
