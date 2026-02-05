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
    api_base_url = "http://localhost:5000"
    db_config = {"host": "localhost", "user": "dbuser", "password": "dbpass", "database": "testdb"} # Example config
    email_log_path = "/var/log/email_service.log" # Example log path
    user_data = {
        "username": "testuser001",
        "email": "testuser001@example.com",
        "password": "SecurePass123!",
        "firstName": "John",
        "lastName": "Doe"
    }
    page = UserRegistrationAPIPage(api_base_url, db_config, email_log_path)
    # Step 1: Register user via API
    api_resp = page.register_user(user_data)
    # Step 2: Validate response schema
    assert api_resp["userId"]
    assert api_resp["username"] == user_data["username"]
    assert api_resp["email"] == user_data["email"]
    assert api_resp["firstName"] == user_data["firstName"]
    assert api_resp["lastName"] == user_data["lastName"]
    assert "registrationTimestamp" in api_resp
    assert "password" not in api_resp
    # Step 3: Verify user in DB
    db_record = page.verify_user_in_db(user_data["username"], user_data["email"])
    assert db_record is not None
    assert db_record["email"] == user_data["email"]
    assert db_record["password"] != user_data["password"]
    assert db_record["account_status"] == "ACTIVE"
    # Step 4: Verify confirmation email
    assert page.verify_confirmation_email(user_data["email"])

# TC-SCRUM-96-010: Cart API Workflow Automation Test
from PageClasses.CartAPIPageClass import CartAPIPageClass

def test_TC_SCRUM_96_010_cart_api():
    """
    Test Case TC-SCRUM-96-010: Cart API Workflow Automation
    Steps:
    1. Sign in as a user who has no existing cart [Test Data: {"email": "newcartuser@example.com", "password": "Pass123!"}]
    2. Send POST request to /api/cart/items to add first product to cart [Test Data: {"productId": "PROD-001", "quantity": 2}]
    3. Verify cart exists in database with correct item and quantity [Test Data: Query: SELECT * FROM carts WHERE userId={userId}; SELECT * FROM cart_items WHERE cartId={cartId}]
    4. Send GET request to /api/cart to retrieve cart details [Test Data: Authorization: Bearer {token}]
    Acceptance Criteria: AC-005
    """
    cart_api = CartAPIPageClass()
    # Step 1: Sign in
    assert cart_api.sign_in("newcartuser@example.com", "Pass123!"), "Sign-in failed"
    # Step 2: Add item to cart
    assert cart_api.add_item_to_cart("PROD-001", 2), "Add item to cart failed"
    # Step 3: Verify cart in DB
    assert cart_api.verify_cart_in_db(db_conn), "Cart DB verification failed"
    # Step 4: Get cart and assert contents
    cart_details = cart_api.get_cart()
    assert cart_details is not None, "Cart retrieval failed"
    assert cart_details['items'][0]['productId'] == "PROD-001", "Product ID mismatch in cart"
    assert cart_details['items'][0]['quantity'] == 2, "Product quantity mismatch in cart"
