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

# TC-SCRUM-96-001: User Registration API, DB, and Email Log Automation Test
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage

def test_TC_SCRUM_96_001_user_registration_api_db_email():
    """
    Test Case TC_SCRUM96_001: User Registration API, DB, and Email Log Automation
    Steps:
    1. Send POST request to /api/users/register with valid user registration data (username, email, password, firstName, lastName)
    2. Validate HTTP 201 response and returned user object (userId, username, email, firstName, lastName, registration timestamp; password not present)
    3. Query database for user record; verify username, correct email, hashed password, and ACTIVE account status
    4. Check email logs for registration confirmation email sent to user
    """
    db_cfg = {"host": "localhost", "user": "root", "password": "pwd", "database": "ecommerce"}
    email_log = "/var/log/email_service.log"
    page = UserRegistrationAPIPage(db_config=db_cfg, email_log_path=email_log)
    username = "testuser001"
    email = "testuser001@example.com"
    password = "SecurePass123!"
    first_name = "John"
    last_name = "Doe"
    result = page.full_workflow(username, email, password, first_name, last_name)
    api_resp = result["api_response"]
    db_record = result["db_record"]
    email_log_result = result["email_log"]
    # Step 2: Validate API response
    assert api_resp["username"] == username, "Username mismatch in API response"
    assert api_resp["email"] == email, "Email mismatch in API response"
    assert api_resp["firstName"] == first_name, "First name mismatch in API response"
    assert api_resp["lastName"] == last_name, "Last name mismatch in API response"
    assert "userId" in api_resp, "userId missing in API response"
    assert "password" not in api_resp, "Password should not be returned in API response"
    # Step 3: Validate DB record
    assert db_record["username"] == username, "Username mismatch in DB"
    assert db_record["email"] == email, "Email mismatch in DB"
    assert db_record["account_status"] == "ACTIVE", f"Account status is not ACTIVE, got {db_record['account_status']}"
    assert db_record["password_hash"] != password, "Password should be hashed in DB"
    # Step 4: Validate email log
    assert email_log_result is True, "Confirmation email not found in logs"
