# TC-SCRUM-96-001: API Signup Automation Test
from auto_scripts.Pages.APISignupPage import APISignupPage

def test_TC_SCRUM_96_001_api_signup():
    ...[existing code continues]...
# TC-SCRUM-96-008: Product Search API Automation Test
from auto_scripts.Pages.ProductSearchPage import ProductSearchPage

def test_TC_SCRUM_96_008_product_search_api():
    """
    Test Case TC-SCRUM-96-008: Product Search API Automation
    Steps:
    1. Send GET request to /api/products/search with search term 'laptop'
    2. Validate HTTP 200 response
    3. Assert all returned products contain 'laptop' in name or description
    4. Validate product schema (productId, name, description, price, availability)
    Acceptance Criteria: AC-004
    """
    base_url = "https://example-ecommerce.com"  # Replace with actual base URL if needed
    search_query = "laptop"
    product_search_page = ProductSearchPage(base_url)
    products = product_search_page.search_and_validate(search_query)
    assert isinstance(products, list), "Expected list of products"
    for idx, product in enumerate(products):
        assert "productId" in product, f"Product at index {idx} missing productId"
        assert "name" in product, f"Product at index {idx} missing name"
        assert "description" in product, f"Product at index {idx} missing description"
        assert "price" in product, f"Product at index {idx} missing price"
        assert "availability" in product, f"Product at index {idx} missing availability"
        name = product.get("name", "").lower()
        description = product.get("description", "").lower()
        assert search_query.lower() in name or search_query.lower() in description, (
            f"Product at index {idx} does not contain '{search_query}' in name or description"
        )
