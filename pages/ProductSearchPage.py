import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ProductSearchPage:
    """
    Page Object Model for Product Search functionality.
    Implements TC_CART_003: Send a product search request with a valid keyword ('laptop') and expect matching products to be returned.
    Strictly follows Selenium Python best practices for code integrity, maintainability, and downstream automation.
    """

    # Locators - these should be loaded from Locators.json in future, but are hardcoded here for initial implementation
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.ID, "search-submit")
    PRODUCT_LIST = (By.CSS_SELECTOR, "div.product-list")
    PRODUCT_ITEM = (By.CSS_SELECTOR, "div.product-list .product-item")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-item .product-name")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.no-results")

    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://example-ecommerce.com/"

    def open_home_page(self):
        """Navigates to the home page where search is available."""
        self.driver.get(self.base_url)

    def perform_search(self, keyword: str) -> bool:
        """
        Performs a product search using the provided keyword.
        Args:
            keyword (str): Search term (e.g., 'laptop')
        Returns:
            bool: True if search was performed successfully
        Raises:
            Exception: If search input/button not found
        """
        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(keyword)
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SEARCH_BUTTON)
            )
            search_button.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            raise Exception(f"Search field/button not found or not interactable: {str(e)}")

    def get_search_results(self) -> list:
        """
        Retrieves the list of product names returned by the search.
        Returns:
            list: List of product names (str)
        """
        try:
            # Wait for results or no-results message
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.presence_of_element_located(self.PRODUCT_LIST),
                    EC.presence_of_element_located(self.NO_RESULTS_MESSAGE)
                )
            )
            product_elements = self.driver.find_elements(*self.PRODUCT_ITEM)
            product_names = []
            for el in product_elements:
                try:
                    name_el = el.find_element(*self.PRODUCT_NAME)
                    product_names.append(name_el.text)
                except NoSuchElementException:
                    continue
            return product_names
        except TimeoutException:
            # Check for no-results message
            try:
                no_results = self.driver.find_element(*self.NO_RESULTS_MESSAGE)
                if no_results.is_displayed():
                    return []
            except NoSuchElementException:
                pass
            raise Exception("Timed out waiting for search results or no-results message.")

    def validate_search_results(self, keyword: str, expected_min_count: int = 1) -> dict:
        """
        Validates that search results match the keyword and acceptance criteria.
        Args:
            keyword (str): Search term used
            expected_min_count (int): Minimum number of products expected
        Returns:
            dict: Validation results with pass/fail and details
        """
        results = {}
        product_names = self.get_search_results()
        results['product_names'] = product_names
        results['result_count'] = len(product_names)
        results['keyword'] = keyword
        # Acceptance criteria: at least one product, all product names contain keyword (case-insensitive)
        results['has_results'] = len(product_names) >= expected_min_count
        results['all_names_match'] = all(keyword.lower() in name.lower() for name in product_names)
        results['pass'] = results['has_results'] and results['all_names_match']
        return results

    def search_and_validate_tc_cart_003(self, keyword: str = "laptop") -> dict:
        """
        Implements TC_CART_003:
        1. Open home page
        2. Perform search with keyword
        3. Validate results
        Returns:
            dict: Stepwise results and validation for downstream automation
        """
        step_results = {}
        try:
            self.open_home_page()
            step_results['home_page_opened'] = True
        except Exception as e:
            step_results['home_page_opened'] = False
            step_results['error'] = f"Failed to open home page: {str(e)}"
            return step_results
        try:
            step_results['search_performed'] = self.perform_search(keyword)
        except Exception as e:
            step_results['search_performed'] = False
            step_results['error'] = f"Failed to perform search: {str(e)}"
            return step_results
        try:
            validation = self.validate_search_results(keyword)
            step_results.update(validation)
        except Exception as e:
            step_results['validation_error'] = str(e)
            step_results['pass'] = False
        return step_results

"""
Executive Summary:
- ProductSearchPage.py automates TC_CART_003 for product search validation.
- Provides atomic methods for search, result retrieval, and validation, enabling robust E2E test automation.

Analysis:
- Implements: home page navigation, search input, result parsing, and keyword-based validation.
- All logic is atomic, robust, and suitable for downstream orchestration.
- Locators are hardcoded for initial version; recommend future migration to Locators.json/config.

Implementation Guide:
1. Instantiate ProductSearchPage with Selenium WebDriver:
       page = ProductSearchPage(driver)
2. Call search_and_validate_tc_cart_003(keyword='laptop') for E2E validation.
3. Analyze returned dict for stepwise results and pass/fail status.

QA Report:
- All imports validated (selenium, time, exceptions).
- Exception handling covers all critical steps.
- Stepwise result dict enables granular reporting.
- Peer review and static analysis recommended before deployment.

Troubleshooting Guide:
- If search field/button not found, check locator accuracy and page load time.
- If no results returned, validate test data and backend availability.
- If product names do not match keyword, check for UI changes or data issues.
- Increase WebDriverWait time for slow environments.

Future Considerations:
- Parameterize locators via Locators.json/config for maintainability.
- Extend validation for multi-keyword and advanced filters.
- Integrate with test reporting and CI/CD for full E2E coverage.
- Add screenshot capture for failed validations.
"""
