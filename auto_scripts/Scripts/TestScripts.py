
# ... (existing imports and code) ...

from auto_scripts.PageClasses.ProfileAPIValidationPage import ProfileAPIValidationPage
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
from auto_scripts.Pages.LoginPage import LoginPage

# ... (existing test classes and methods) ...

def test_tc_login_001_invalid_credentials(driver):
    """
    Test Case TC_LOGIN_001: Test login functionality with invalid credentials.
    Steps:
        1. Navigate to the login screen.
        2. Enter an invalid username and/or password.
        3. Verify error message 'Invalid username or password. Please try again.' is displayed.
    Acceptance Criteria:
        - Login screen is displayed successfully.
        - Invalid credentials trigger appropriate error message.
        - Error message matches expected text exactly.
    Args:
        driver: Selenium WebDriver instance.
    Raises:
        AssertionError: If any validation fails.
    """
    try:
        # Initialize LoginPage
        login_page = LoginPage(driver)
        
        # Step 1: Navigate to the login screen
        login_displayed = login_page.navigate_to_login_screen()
        assert login_displayed, "Login screen is not displayed after navigation."
        
        # Step 2: Enter invalid username and/or password
        invalid_username = "invalid_user@example.com"
        invalid_password = "wrongpassword123"
        login_page.login_with_invalid_credentials(invalid_username, invalid_password)
        
        # Step 3: Verify error message
        expected_error = "Invalid username or password. Please try again."
        error_displayed = login_page.verify_invalid_login_error(expected_error)
        assert error_displayed, f"Expected error message '{expected_error}' was not displayed correctly."
        
    except Exception as e:
        # Log error and fail the test
        import traceback
        traceback.print_exc()
        assert False, f"Test TC_LOGIN_001 failed: {str(e)}"


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


def test_tc_scrum96_009_product_search_api(driver, db_connection, api_base_url):
    """
    Test Case TC_SCRUM96_009: Product Search API - DB validation and API search parameter handling.
    Steps:
        1. Ensure products table contains at least 5 test products.
        2. Send GET request to /api/products/search?query= (empty query parameter).
        3. Send GET request to /api/products/search without query parameter.
    Acceptance Criteria:
        - DB contains >=5 products.
        - API returns 200 OK with all products or empty array for empty query.
        - API returns 400 Bad Request or all products for missing query param.
    Args:
        driver: Selenium WebDriver instance (not used directly here, but required for test runner compatibility).
        db_connection: Database connection object for validation.
        api_base_url: Base URL for the API endpoints.
    Raises:
        AssertionError: If any validation fails.
    """
    try:
        # Step 1: Ensure DB has at least 5 products
        product_page = ProductSearchAPIPage(db_config=db_connection.db_config, api_base_url=api_base_url)
        product_count = product_page.get_product_count()
        assert product_count >= 5, f"Expected at least 5 products in DB, found {product_count}."
        # Step 2: API search with empty query parameter
        status_empty, data_empty = product_page.search_products_empty_query()
        assert status_empty == 200, f"Expected HTTP 200 OK for empty query, got {status_empty}."
        assert isinstance(data_empty, (dict, list)), f"API response for empty query should be dict or list, got {type(data_empty)}."
        # Step 3: API search with missing query parameter
        status_no_query, data_no_query = product_page.search_products_no_query()
        assert status_no_query in [200, 400], f"Expected HTTP 200 OK or 400 Bad Request for missing query, got {status_no_query}."
        if status_no_query == 400:
            assert "query" in str(data_no_query).lower() or "error" in str(data_no_query).lower(), "Error message for missing query should mention query parameter."
        else:
            assert isinstance(data_no_query, (dict, list)), f"API response for missing query should be dict or list, got {type(data_no_query)}."
    except Exception as e:
        import traceback
        traceback.print_exc()
        assert False, f"Test TC_SCRUM96_009 failed: {str(e)}"
