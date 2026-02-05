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
