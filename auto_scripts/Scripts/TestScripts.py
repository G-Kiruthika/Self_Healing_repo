<existing TestScripts.py content>

def test_TC_SCRUM_96_001_user_signup_api_and_db_validation():
    """
    Test Case TC-SCRUM-96-001: User Signup API & Database Validation
    Steps:
    1. Send POST request to /api/users/signup with valid user data.
    2. Validate response for HTTP 201 and user details.
    3. Verify user data is stored in database.
    4. Ensure response contains userId, username, email but excludes password.
    """
    from PageClasses.UserSignupAPIPage import UserSignupAPIPage
    from PageClasses.DatabaseValidationPage import DatabaseValidationPage
    import requests

    # Setup test data
    base_url = 'http://localhost:8000'  # Adjust as needed
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'user': 'your_db_user',
        'password': 'your_db_password',
        'dbname': 'your_db_name'
    }
    user_data = {
        'username': 'testuser123',
        'email': 'testuser@example.com',
        'password': 'SecurePass123!'
    }
    expected_schema = {
        'userId': int,
        'username': str,
        'email': str
    }
    sensitive_keys = ['password']

    # Step 1: Signup user via API
    signup_page = UserSignupAPIPage(base_url)
    response = signup_page.signup_user(user_data)

    # Step 2: Validate response
    assert response.status_code == 201, f"Expected HTTP 201, got {response.status_code}"
    assert signup_page.validate_response_schema(response, expected_schema), "Response schema invalid"
    assert signup_page.ensure_no_sensitive_data(response, sensitive_keys), "Sensitive data exposed in response"
    resp_json = response.json()
    assert resp_json['username'] == user_data['username'], "Username mismatch"
    assert resp_json['email'] == user_data['email'], "Email mismatch"

    # Step 3: Verify user in database
    db_page = DatabaseValidationPage(db_config)
    assert db_page.verify_user_in_db(user_data['email']), "User record not found in DB"
