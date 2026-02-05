
# ... (existing imports and code) ...

from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage

# ... (existing test classes and methods) ...

def test_tc_scrum96_007_profile_api_validation(driver, db_connection):
    """
    Test Case TC_SCRUM96_007: Profile API returns correct user profile and excludes password.

    Steps:
        1. Register and login a test user to obtain a valid JWT authentication token.
        2. Send GET request to /api/users/profile endpoint with valid JWT token in Authorization header.
        3. Verify all profile fields match the registered user data in database and password is not present in API response.

    Acceptance Criteria:
        - User is registered and logged in successfully with valid JWT token.
        - API returns HTTP 200 OK with complete user profile (userId, username, email, firstName, lastName, registrationDate, accountStatus). Password is not included.
        - Profile data returned matches database records exactly for all fields.

    Args:
        driver: Selenium WebDriver instance.
        db_connection: Database connection object for validation.

    Raises:
        AssertionError: If any validation fails.
    """
    try:
        # Test Data
        user_data = {
            "username": "profileuser",
            "email": "profileuser@example.com",
            "password": "Profile123!",
            "firstName": "Profile",
            "lastName": "User"
        }

        # Step 1: Register and login user to obtain JWT
        profile_page = ProfileAPIValidationPage(driver)
        jwt_token = profile_page.register_and_login(user_data)
        assert jwt_token is not None and isinstance(jwt_token, str), "Failed to obtain JWT token after registration/login."

        # Step 2: Call profile API
        response = profile_page.get_profile(jwt_token)
        assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."
        profile_json = response.json()

        # Step 3: Validate profile fields
        # Fetch user from DB
        cursor = db_connection.cursor()
        cursor.execute("SELECT userId, username, email, firstName, lastName, registrationDate, accountStatus, password FROM users WHERE username = %s", (user_data["username"],))
        db_user = cursor.fetchone()
        assert db_user is not None, "User not found in database."

        db_fields = ["userId", "username", "email", "firstName", "lastName", "registrationDate", "accountStatus"]
        for idx, field in enumerate(db_fields):
            api_value = profile_json.get(field)
            db_value = db_user[idx]
            assert api_value == db_value, f"Mismatch for {field}: API={api_value}, DB={db_value}"

        # Ensure password is not present in API response
        assert "password" not in profile_json, "Password field should not be present in API response."

    except Exception as e:
        # Log error and fail the test
        import traceback
        traceback.print_exc()
        assert False, f"Test TC_SCRUM96_007 failed: {str(e)}"
