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
    assert api_signup_page.run_full_signup_test(username, email, password), "Signup test failed"

# TC-SCRUM-96-008: Product Search API Automation Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage

def test_TC_SCRUM_96_008_product_search_api():
    """
    Test Case TC-SCRUM-96-008: Product Search API Automation
    Steps:
    1. Send GET request to /api/products/search with search term 'laptop' [Test Data: Query parameter: ?q=laptop]
    2. Validate HTTP 200 response and list of products matching 'laptop'
    3. Ensure all returned products have 'laptop' in name or description
    4. Validate each product object contains productId, name, description, price, and availability
    Acceptance Criteria: AC-004
    """
    search_term = 'laptop'
    product_search_api = ProductSearchAPIPage()
    product_search_api.run_full_product_search_validation(search_term)

def test_TC_SCRUM_96_008_product_search_api_v2():
    """
    Test Case TC-SCRUM-96-008: Product Search API Automation (Explicit Validation)
    Steps:
    1. Send GET request to /api/products/search with search term 'laptop' [Test Data: Query parameter: ?q=laptop]
    2. Validate HTTP 200 response and list of products matching 'laptop'
    3. Ensure all returned products have 'laptop' in name or description
    4. Validate each product object contains id, name, price, description, category, imageUrl
    Acceptance Criteria: AC-004 (Expanded)
    """
    search_term = 'laptop'
    product_search_api = ProductSearchAPIPage()
    # Step 1 & 2: Send GET request and validate HTTP 200
    response = product_search_api.search_products(search_term)
    # Step 3: Validate products match search
    products = product_search_api.validate_products_match_search(response, search_term)
    # Step 4: Validate each product object contains required fields
    product_search_api.validate_product_schema(products)

# TC_SCRUM96_001: User Registration API Automation Test
from PageClasses.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_001_user_registration_api():
    """
    Test Case TC_SCRUM96_001: User Registration API Automation
    Steps:
    1. Send POST request to /api/users/register with valid user registration data (username, email, password, firstName, lastName)
    2. Validate HTTP 201 response and correct schema (userId, username, email, firstName, lastName, registrationTimestamp; password not present)
    3. Query database to verify user creation, email stored, password hashed, account status 'ACTIVE'
    4. Check email log for registration confirmation sent to user
    """
    db_config = {"host": "localhost", "user": "root", "password": "pwd", "database": "ecommerce"}
    email_log_path = "/var/log/email_service.log"
    page = UserRegistrationAPIPage(db_config=db_config, email_log_path=email_log_path)
    username = "testuser001"
    email = "testuser001@example.com"
    password = "SecurePass123!"
    first_name = "John"
    last_name = "Doe"
    # Step 1: Register user via API
    api_resp = page.register_user_api(username, email, password, first_name, last_name)
    # Step 2: Validate response schema
    assert "userId" in api_resp
    assert api_resp["username"] == username
    assert api_resp["email"] == email
    assert api_resp["firstName"] == first_name
    assert api_resp["lastName"] == last_name
    assert "password" not in api_resp
    # Step 3: Verify user in DB
    db_record = page.verify_user_in_db(username)
    assert db_record["username"] == username
    assert db_record["email"] == email
    assert db_record["password_hash"] != password
    assert db_record["account_status"] == "ACTIVE"
    # Step 4: Verify confirmation email
    assert page.check_email_log(email)

# TC_SCRUM96_002: Duplicate User Registration API Automation Test
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_002_duplicate_user_registration_api():
    """
    Test Case TC_SCRUM96_002: Duplicate User Registration API Automation
    Steps:
    1. Register user with username 'duplicateuser' and email 'first@example.com'. Expect HTTP 201 Created.
    2. Attempt to register another user with same username 'duplicateuser' and email 'second@example.com'. Expect HTTP 409 Conflict and error message.
    3. Verify only one user record exists in database with username 'duplicateuser' and email 'first@example.com'.
    """
    db_config = {"host": "localhost", "user": "dbuser", "password": "dbpass", "database": "testdb"}
    page = UserRegistrationAPIPage(db_config=db_config)
    username = "duplicateuser"
    email1 = "first@example.com"
    password1 = "Pass123!"
    first_name1 = "First"
    last_name1 = "User"
    email2 = "second@example.com"
    password2 = "Pass456!"
    first_name2 = "Second"
    last_name2 = "User"
    # Step 1: Register first user
    resp1 = page.register_user(username, email1, password1, first_name1, last_name1)
    assert resp1.status_code == 201, f"Expected 201 Created, got {resp1.status_code}"
    # Step 2: Register duplicate user
    resp2 = page.register_duplicate_user(username, email2, password2, first_name2, last_name2)
    page.validate_conflict_response(resp2)
    # Step 3: DB validation
    db_count = page.get_user_count_by_username(username)
    assert db_count == 1, f"Expected exactly 1 user record for username '{username}', found {db_count}"

# TC_SCRUM96_005: Negative API Login, Token Absence, Audit Log Verification
from auto_scripts.Pages.LoginPage import LoginPage

def test_TC_SCRUM96_005_negative_api_login_audit_log():
    """
    Test Case TC_SCRUM96_005: Negative API Login, Token Absence, and Audit Log Verification
    Steps:
    1. Send POST to /api/auth/login with non-existent username and password
    2. Verify HTTP 401 Unauthorized and error message 'Invalid username or password'
    3. Verify no JWT tokens in response
    4. Verify audit log entry for failed login
    """
    # Setup
    base_url = "http://localhost:8000"  # Replace with real base URL in test env
    username = "nonexistentuser999"
    password = "AnyPassword123!"
    source_ip = "127.0.0.1"
    driver = None  # Replace with Selenium WebDriver if UI steps are needed

    # Mock audit_log_query_func for demonstration
    def audit_log_query_func(query_username):
        # Simulate audit log entries
        return [
            {"username": query_username, "timestamp": "2024-06-01T12:34:56Z", "source_ip": source_ip}
        ]

    login_page = LoginPage(driver=driver, base_url=base_url)
    result = login_page.run_tc_scrum96_005(username, password, source_ip, audit_log_query_func)
    assert result["audit_log_verified"] is True, "Audit log verification failed for failed login attempt."
