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
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM96_001_user_registration_api():
    """
    Test Case TC_SCRUM96_001: User Registration API Automation
    Steps:
    1. Send POST request to /api/users/register with valid user registration data (username, email, password, firstName, lastName)
    2. Validate HTTP 201 response and correct schema (userId, username, email, firstName, lastName, registrationTimestamp; password not present)
    3. Query database to verify user creation, email stored, password hashed, account status 'ACTIVE'
    4. Check email log for registration confirmation sent to user
    """
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "pwd",
        "database": "ecommerce"
    }
    email_log_path = "/var/log/email_service.log"
    page = UserRegistrationAPIPage(db_config=db_config, email_log_path=email_log_path)
    username = "testuser001"
    email = "testuser001@example.com"
    password = "SecurePass123!"
    first_name = "John"
    last_name = "Doe"
    # Step 1, 2, 3, 4: End-to-end workflow
    result = page.full_workflow(username, email, password, first_name, last_name)
    # Step 2: Validate API response
    api_resp = result["api_response"]
    assert api_resp["userId"], "userId missing in API response"
    assert api_resp["username"] == username, "Username mismatch in API response"
    assert api_resp["email"] == email, "Email mismatch in API response"
    assert api_resp["firstName"] == first_name, "First name mismatch in API response"
    assert api_resp["lastName"] == last_name, "Last name mismatch in API response"
    assert "password" not in api_resp, "Password should not be in API response"
    # Step 3: Validate DB record
    db_record = result["db_record"]
    assert db_record["username"] == username, "Username mismatch in DB"
    assert db_record["email"] == email, "Email mismatch in DB"
    assert db_record["password_hash"] != password, "Password should be hashed in DB"
    assert db_record["account_status"] == "ACTIVE", "Account status should be ACTIVE"
    # Step 4: Validate email log
    assert result["email_log"] is True, "Confirmation email not found in logs"

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
    # Step 1 & 2: Register first user, then attempt duplicate
    resp_json1, resp_json2 = page.register_duplicate_user_and_validate(
        username, email1, password1, first_name1, last_name1,
        email2, password2, first_name2, last_name2
    )
    assert resp_json1["username"] == username
    assert resp_json1["email"] == email1
    assert "userId" in resp_json1
    assert resp_json2["error"]
    assert "username already exists" in resp_json2["error"].lower()
    # Step 3: DB validation
    db_record = page.verify_single_user_record_in_db(username, email1)
    assert db_record["count"] == 1
    assert db_record["email"] == email1
