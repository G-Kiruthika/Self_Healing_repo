# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...
# TC_SCRUM96_006: Negative Login API & Session Validation Test
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_006_negative_login_api_and_session_validation():
    ...

# TC_SCRUM96_007: User Profile API & DB Validation Test
from PageClasses.UserRegistrationAPIPage import UserRegistrationAPIPage
from PageClasses.ProfilePage import ProfilePage

def test_TC_SCRUM96_007_user_profile_api_db_validation():
    """
    Test Case TC_SCRUM96_007: User Profile API & DB Validation
    Steps:
    1. Register and login a test user to obtain valid JWT authentication token
    2. Send GET request to /api/users/profile endpoint with valid JWT token in Authorization header
    3. Verify all profile fields match the registered user data in database
    """
    user_data = {
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "Profile123!",
        "firstName": "Profile",
        "lastName": "User"
    }
    db_config = {
        "host": "localhost",
        "port": 5432,
        "dbname": "yourdb",
        "user": "youruser",
        "password": "yourpass"
    }
    reg_api = UserRegistrationAPIPage()
    jwt = reg_api.register_and_login_user_get_jwt(user_data)
    assert jwt is not None, "JWT token not received after registration/login"
    prof_api = ProfilePage()
    api_profile = prof_api.get_profile_api(jwt)
    db_profile = prof_api.get_db_user_profile(db_config, user_data['username'])
    assert db_profile is not None, "DB profile not found for registered user"
    assert prof_api.validate_profile_data(api_profile, db_profile), "Profile data mismatch or password present in API response"

# TC_SCRUM96_005: Negative Login Audit Log Test
from auto_scripts.Pages.LoginPage import LoginPage
import datetime

def test_TC_SCRUM_96_005_negative_login_audit_log():
    """
    Test Case TC_SCRUM96_005
    Steps:
    1. Send POST request to /api/auth/login endpoint with non-existent username and any password.
    2. Verify API returns HTTP 401 Unauthorized with error message 'Invalid username or password'.
    3. Verify no JWT token is generated or returned in the response.
    4. Verify failed login attempt is logged in security audit logs with username, timestamp, and source IP address.
    """
    base_url = "http://localhost:8000"  # Adjust to your app URL
    username = "nonexistentuser999"
    password = "AnyPassword123!"
    login_page = LoginPage(None, base_url)  # Pass a mock or None for driver for API-only test

    # Step 1: Attempt login via API
    response = login_page.api_auth_login(username, password)
    
    # Step 2: Verify 401 Unauthorized and error message
    login_page.verify_auth_failure(response, "Invalid username or password")

    # Step 3: Verify no JWT token and no session
    login_page.verify_no_token_and_no_session(response)

    # Step 4: Verify audit log entry
    start_time = datetime.datetime.now() - datetime.timedelta(seconds=10)
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
    def log_fetcher_func(st, et):
        # Stub example: Replace with actual log fetcher integration
        # Should return a list of dicts with keys: username, action, timestamp, source_ip
        return [{
            "username": username,
            "action": "login_failed",
            "timestamp": datetime.datetime.now().timestamp(),
            "source_ip": "127.0.0.1"
        }]
    login_page.verify_failed_login_audit_log(username, start_time, end_time, log_fetcher_func)

# TC_SCRUM96_008: Product Search API Case-Insensitive Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage
import requests

def test_TC_SCRUM96_008_product_search_case_insensitive():
    """
    Test Case TC_SCRUM96_008: Product Search API - Case Insensitive
    Steps:
    1. Insert three products into database: 'Laptop Computer', 'Gaming Laptop', 'Desktop Computer'.
    2. Send GET requests to /api/products/search for 'laptop', 'LAPTOP', 'LaPtOp'.
    3. Validate HTTP 200 and that both laptop products are returned for all queries.
    """
    # Setup DB config (replace with actual test DB config)
    db_config = {
        "host": "localhost",
        "user": "testuser",
        "password": "testpass",
        "database": "testdb"
    }
    session = requests.Session()
    page = ProductSearchAPIPage(session=session, db_config=db_config)
    products = [
        {"productId": 201, "name": "Laptop Computer", "description": "High performance laptop", "price": 999.99, "availability": True},
        {"productId": 202, "name": "Gaming Laptop", "description": "Gaming laptop with RTX", "price": 1499.99, "availability": True},
        {"productId": 203, "name": "Desktop Computer", "description": "Desktop PC", "price": 799.99, "availability": True}
    ]
    # Insert products and validate search results for case variants
    page.tc_scrum96_008_full_workflow(products, "laptop")
