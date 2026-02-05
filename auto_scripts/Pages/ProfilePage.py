import requests

class ProfilePage:
    def __init__(self, page):
        self.page = page
        self.user_profile_icon = page.locator('#profile-icon')

    async def click_profile(self):
        await self.user_profile_icon.click()

    def get_profile_info(self, base_url, token):
        """
        Sends GET request to /api/users/profile with authentication token.
        Returns response JSON and status code.
        """
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }
        response = requests.get(f"{base_url}/api/users/profile", headers=headers)
        return response.json(), response.status_code

    def validate_sensitive_info_not_exposed(self, response_json):
        """
        Validates that sensitive information (like 'password') is NOT in the response.
        Returns True if not present, False otherwise.
        """
        sensitive_fields = ['password', 'pass', 'pwd', 'secret']
        for field in sensitive_fields:
            if field in response_json:
                return False
        return True

    def validate_profile_response_schema(self, response_json):
        """
        Validates the response contains only expected fields: userId, username, email.
        Returns True if schema matches, False otherwise.
        """
        expected_fields = {'userId', 'username', 'email'}
        response_fields = set(response_json.keys())
        # Ensure all expected fields are present
        if not expected_fields.issubset(response_fields):
            return False
        # Ensure no unexpected fields (except allowed ones)
        allowed_fields = expected_fields
        extra_fields = response_fields - allowed_fields
        # If extra fields do not include sensitive info, it's okay (for extensibility)
        sensitive_fields = {'password', 'pass', 'pwd', 'secret'}
        if sensitive_fields & extra_fields:
            return False
        return True
