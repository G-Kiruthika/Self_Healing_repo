class ProfilePage:
    def __init__(self, page):
        self.page = page
        self.user_profile_icon = page.locator('#profile-icon')

    async def click_profile(self):
        await self.user_profile_icon.click()

    def get_profile_api(self, token):
        """
        Sends GET request to /api/users/profile with authentication token.
        Returns response JSON if successful, else raises exception.
        """
        import requests
        url = 'https://example-ecommerce.com/api/users/profile'
        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    def validate_profile_response(self, response_json):
        """
        Validates response contains userId, username, email and does NOT contain password or other sensitive data.
        Raises AssertionError if validation fails.
        """
        required_fields = ['userId', 'username', 'email']
        forbidden_fields = ['password', 'ssn', 'creditCard', 'token', 'secret']
        # Check required fields
        for field in required_fields:
            if field not in response_json:
                raise AssertionError(f"Missing required field in response: {field}")
        # Check forbidden fields
        for field in forbidden_fields:
            if field in response_json:
                raise AssertionError(f"Sensitive field exposed in response: {field}")
        # Basic type validation
        if not isinstance(response_json['userId'], (int, str)):
            raise AssertionError("userId must be int or str")
        if not isinstance(response_json['username'], str):
            raise AssertionError("username must be str")
        if not isinstance(response_json['email'], str):
            raise AssertionError("email must be str")
        # Email format validation
        import re
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", response_json['email']):
            raise AssertionError("Invalid email format in profile response")
        return True
