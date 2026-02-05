# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    """
    Test Case TC-SCRUM-96-001: API Signup Automation
    Steps:
    1. Send POST request to /api/users/signup with valid user data (username, email, password)
    2. Validate HTTP 201 response and correct schema (userId, username, email, no password)
    3. Verify user data is stored in database with hashed password and correct details
    """
    username = "testuser123"
    email = "testuser@example.com"
    password = "SecurePass123!"
    api_signup_page = APISignupPage()
    # End-to-end test
    assert api_signup_page.run_full_signup_test(username, email, password), "Signup test failed"

# TC-SCRUM-96-001: User Signup Flow with UserSignupPage
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_001_user_signup_flow():
    """
    Test Case TC-SCRUM-96-001: User Signup Flow
    Steps:
    1. Send POST request to /api/users/signup with valid user data
    2. Validate HTTP 201 response and correct schema
    3. Verify user data is stored in simulated DB with hashed password
    """
    username = "testuser123"
    email = "testuser@example.com"
    password = "SecurePass123!"
    signup_page = UserSignupPage()
    signup_page.run_signup_flow(username, email, password)

# TC-LOGIN-008: Minimum allowed length for login credentials
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC_LOGIN_008_min_length_login(driver):
    """
    Test Case TC_LOGIN_008: Minimum allowed length for login credentials
    Steps:
    1. Navigate to the login page.
    2. Enter email and password with minimum allowed length (email: a@b.co, password: 123456).
    3. Click Login and assert login is accepted if credentials are valid.
    Acceptance Criteria: 8
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_min_length_accepted("a@b.co", "123456"), "Minimum length credentials were not accepted."

# TC-SCRUM-96-002: Duplicate Email Signup Handling
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_002_duplicate_email_signup():
    """
    Test Case TC-SCRUM-96-002: Duplicate Email Signup Handling
    Steps:
    1. Create user with email testuser@example.com (username: user1, password: Pass123!)
    2. Attempt to create another user with same email (username: user2, password: Pass456!)
    3. Verify only one user record exists in simulated DB for that email
    Acceptance criteria: Registration fails with 409 Conflict and error message 'Email already exists', DB contains only one record.
    """
    signup_page = UserSignupPage()
    signup_page.signup_duplicate_email_test()

# TC-SCRUM-96-003: Invalid Email Signup Automation Test
from auto_scripts.Pages.UserSignupPage import UserSignupPage

def test_TC_SCRUM_96_003_invalid_email_signup(driver, db_connection):
    """
    Test Case TC-SCRUM-96-003: Invalid Email Signup Automation
    Steps:
    1. Send POST request to /api/users/signup with invalid email format (username: testuser, email: invalidemail, password: Pass123!)
    2. Validate HTTP 400 response and error messaging
    3. Perform equivalent UI flow and check for error message
    4. Query database to confirm no user record was created
    """
    signup_page = UserSignupPage(driver)
    result = signup_page.signup_with_invalid_email_and_validate(
        invalid_email="invalidemail",
        username="testuser",
        password="Pass123!",
        db_connection=db_connection
    )
    assert result["db_user_count"] == 0, f"User with invalid email should not be created. Found {result['db_user_count']} records."
    assert "invalid email" in result["ui_error_message"].lower() or "email format" in result["ui_error_message"].lower(), f"Expected email format error in UI, got: {result['ui_error_message']}"
    assert "invalid email" in result["api_response"].lower() or "email format" in result["api_response"].lower(), f"Expected email format error in API response, got: {result['api_response']}"

# TC-SCRUM-96-004: Login and JWT Validation Automation Test
from auto_scripts.Pages.UserSignupPage import UserSignupPage
from auto_scripts.Pages.LoginPage import LoginPage
import requests

def test_TC_SCRUM_96_004_login_and_jwt_validation(driver):
    """
    Executive Summary:
    - This test automates the end-to-end workflow for user account creation, login, and JWT authentication validation.
    - It covers the acceptance criteria for TC-SCRUM-96-004, ensuring robust quality assurance and future maintainability.

    Detailed Analysis:
    - Step 1: Create a user account using UserSignupPage with valid credentials.
    - Step 2: Authenticate via API (POST /api/users/signin) and validate HTTP 200 response and token presence.
    - Step 3: Decode and validate the returned JWT token using LoginPage.validate_jwt_token.

    Implementation Guide:
    - Uses Selenium Page Object Model for UI actions and requests library for API calls.
    - Leverages LoginPage.validate_jwt_token for secure token verification.
    - Extensible for future authentication flows and token claims.

    Quality Assurance Report:
    - Asserts on user creation, successful login, and JWT validity.
    - Error handling for API and token validation.
    - Full traceability in logs and comments.

    Troubleshooting Guide:
    - If user creation fails, check DB and API endpoint.
    - If login fails, verify credentials and API status.
    - If JWT validation fails, check token format and claims.

    Future Considerations:
    - Easily extend to multi-factor authentication and additional JWT claims.
    - Modular structure for integration with CI/CD pipelines.
    """
    # Test data
    username = "loginuser"
    email = "login@example.com"
    password = "LoginPass123!"

    # Step 1: Create user account
    signup_page = UserSignupPage(driver)
    signup_result = signup_page.register_user(username, email, password)
    assert signup_result["status"] == "success", f"User creation failed: {signup_result}"

    # Step 2: Authenticate via API and retrieve JWT token
    signin_api_url = "https://example-ecommerce.com/api/users/signin"
    signin_payload = {"email": email, "password": password}
    signin_response = requests.post(signin_api_url, json=signin_payload)
    assert signin_response.status_code == 200, f"Sign-in failed: {signin_response.text}"
    response_json = signin_response.json()
    assert "token" in response_json, "Authentication token not found in response."
    token = response_json["token"]

    # Step 3: Validate JWT token
    validated_payload = LoginPage.validate_jwt_token(token)
    assert "userId" in validated_payload, "userId missing in JWT payload."
    assert "email" in validated_payload, "email missing in JWT payload."
    assert "exp" in validated_payload, "Expiration time missing in JWT payload."
    # Additional assertion for expiration
    import datetime
    exp_time = datetime.datetime.fromtimestamp(validated_payload["exp"])
    assert exp_time > datetime.datetime.utcnow(), "Token has expired."

# TC016: Session Timeout Automation Test
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC016_session_timeout_logout(driver):
    """
    Test Case TC016: Session Timeout
    Steps:
    1. Login and remain inactive for session timeout duration.
       [Test Data: user@example.com / ValidPassword123]
    2. Verify user is automatically logged out after timeout.
    Acceptance Criteria: User is redirected to login page or session expired message is shown.
    """
    email = "user@example.com"
    password = "ValidPassword123"
    login_page = LoginPage(driver)
    login_page.login_with_credentials(email, password)
    # Simulate inactivity and verify logout
    assert login_page.wait_for_session_timeout_and_verify_logout(timeout_duration=900), "User was not logged out after session timeout."

# TC-SCRUM-96-005: API Signin Negative Test
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC_SCRUM_96_005_api_signin_invalid_credentials():
    """
    Test Case TC-SCRUM-96-005: API Sign-in Negative Test
    Steps:
    1. Ensure user account exists with known credentials (email: login@example.com, password: LoginPass123!)
    2. Send POST request to /api/users/signin with incorrect password (email: login@example.com, password: WrongPassword)
    3. Verify sign-in fails with HTTP 401 Unauthorized and error message 'Invalid credentials'
    4. Verify no authentication token is returned
    Acceptance Criteria: As described above
    """
    email = "login@example.com"
    invalid_password = "WrongPassword"
    result = LoginPage.api_signin_invalid_credentials(email, invalid_password)
    assert result["status_code"] == 401, f"Expected HTTP 401 Unauthorized, got {result['status_code']}"
    assert "invalid credentials" in result["error_message"].lower(), f"Expected error message 'Invalid credentials', got '{result['error_message']}'"
    assert not result["token_present"], f"Expected no authentication token, but got one."
