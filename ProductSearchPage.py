import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class ProductSearchPage:
    """
    Page Object for product search functionality in Selenium automation.
    Implements search_products(keyword) and validate_search_results(expected_keyword) for TC_CART_003.
    Strictly follows Python best practices for maintainability and downstream automation.
    """
    SEARCH_INPUT_LOCATOR = (By.ID, "search-input")
    SEARCH_BUTTON_LOCATOR = (By.ID, "search-btn")
    PRODUCT_LIST_LOCATOR = (By.CSS_SELECTOR, ".product-list .product-item")
    SEARCH_API_URL = "https://example-ecommerce.com/api/products/search"

    def __init__(self, driver: WebDriver):
        """
        Initializes ProductSearchPage with Selenium WebDriver.
        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        self.driver = driver

    def search_products_ui(self, keyword: str):
        """
        Sends a product search request via UI with the provided keyword.
        Args:
            keyword (str): Product search keyword
        Raises:
            RuntimeError: If UI elements are not found or interaction fails
        """
        try:
            search_input = self.driver.find_element(*self.SEARCH_INPUT_LOCATOR)
            search_input.clear()
            search_input.send_keys(keyword)
            search_btn = self.driver.find_element(*self.SEARCH_BUTTON_LOCATOR)
            search_btn.click()
        except (NoSuchElementException, WebDriverException) as e:
            raise RuntimeError(f"UI search failed: {e}")

    def get_search_results_ui(self):
        """
        Retrieves product search results from UI.
        Returns:
            list[str]: List of product names displayed
        Raises:
            RuntimeError: If product items cannot be retrieved
        """
        try:
            products = self.driver.find_elements(*self.PRODUCT_LIST_LOCATOR)
            product_names = [p.text.strip() for p in products if p.text.strip()]
            return product_names
        except (NoSuchElementException, WebDriverException) as e:
            raise RuntimeError(f"Failed to fetch product items from UI: {e}")

    def validate_search_results_ui(self, expected_keyword: str):
        """
        Validates that all product names in search results contain the expected keyword.
        Args:
            expected_keyword (str): Keyword to validate in product names
        Returns:
            bool: True if all products match, raises AssertionError otherwise
        """
        product_names = self.get_search_results_ui()
        if not product_names:
            raise AssertionError("No products found in UI search results.")
        for name in product_names:
            assert expected_keyword.lower() in name.lower(), (
                f"Product '{name}' does not match search keyword '{expected_keyword}'"
            )
        return True

    def search_products_api(self, keyword: str):
        """
        Sends a product search request to the API endpoint with the provided keyword.
        Args:
            keyword (str): Product search keyword
        Returns:
            list[dict]: List of product dicts from API response
        Raises:
            RuntimeError: If API call fails or response is invalid
        """
        payload = {"search": keyword}
        try:
            response = requests.post(self.SEARCH_API_URL, json=payload, timeout=10)
            response.raise_for_status()
            products = response.json().get("products", [])
            if not isinstance(products, list):
                raise RuntimeError("API response 'products' is not a list.")
            return products
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API search request failed: {e}")
        except Exception as e:
            raise RuntimeError(f"API response parsing failed: {e}")

    def validate_search_results_api(self, products: list, expected_keyword: str):
        """
        Validates that all API product names contain the expected keyword.
        Args:
            products (list): List of product dicts from API
            expected_keyword (str): Keyword to validate in product names
        Returns:
            bool: True if all products match, raises AssertionError otherwise
        """
        if not products:
            raise AssertionError("No products found in API search results.")
        for product in products:
            name = product.get("name", "")
            assert expected_keyword.lower() in name.lower(), (
                f"API product '{name}' does not match search keyword '{expected_keyword}'"
            )
        return True

"""
Executive Summary:
- Added ProductSearchPage.py to support TC_CART_003: Product search and result validation.
- Enables robust UI and API search automation with strict validation and error handling.

Detailed Analysis:
- Implements both UI-driven and API-driven product search methods for regression and integration testing.
- Validates product search results against the provided keyword, ensuring downstream data integrity.
- Follows strict locator strategy and handles common Selenium/WebDriver exceptions.

Implementation Guide:
1. Initialize ProductSearchPage(driver) with Selenium WebDriver instance.
2. Call search_products_ui(keyword) to perform UI search, then validate_search_results_ui(expected_keyword) to validate UI results.
3. Call search_products_api(keyword) to perform API search, then validate_search_results_api(products, expected_keyword) to validate API results.
4. Integrate these methods in your test automation pipeline for end-to-end coverage.

Quality Assurance Report:
- All imports verified for compatibility with Selenium and requests.
- Exception handling covers UI and API failure scenarios.
- Assertions ensure strict matching of expected data.
- Peer review and integration testing recommended before production deployment.

Troubleshooting Guide:
- If UI search fails, check locator values and page load timing.
- If API search fails, verify endpoint URL and backend status.
- For assertion errors, validate test data and expected keyword.
- For network issues, confirm connectivity and retry logic.

Future Considerations:
- Parameterize locators and URLs for multi-environment support.
- Extend validation for product attributes (price, category, etc.).
- Add support for paginated or filtered search results.
- Integrate with self-healing locator framework for enhanced resilience.
"""
