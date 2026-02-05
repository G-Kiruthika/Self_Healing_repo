# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...
# [rest of content as above]

# TC-SCRUM-96-008: Product Search API Automation Test
from auto_scripts.Pages.ProductSearchAPIPage import ProductSearchAPIPage

def test_TC_SCRUM_96_008_product_search_api():
    """
    Test Case TC-SCRUM-96-008: Product Search API Automation
    Steps:
    1. Send GET request to /api/products/search with search term 'laptop'.
    2. Validate HTTP 200 response and that all returned products contain 'laptop' in name or description.
    3. Verify product details include productId, name, description, price, and availability.
    """
    search_term = 'laptop'
    product_search_api = ProductSearchAPIPage()
    product_search_api.run_full_product_search_validation(search_term)
