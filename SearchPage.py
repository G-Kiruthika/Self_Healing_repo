# SearchPage.py
"""
PageClass for product search functionality (TC_CART_003)
Implements methods to search for products and validate search results.
Assumed locators are documented for downstream refinement.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from typing import List

class SearchPage:
    """
    Page Object Model for the product search page.
    """
    # Assumed locators (update as needed)
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='q']")  # Search box
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")  # Search button
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-title")  # Product result titles

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def search_product(self, keyword: str):
        """
        Enters the search keyword and submits the search.
        :param keyword: The product keyword to search for.
        """
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(keyword)
        # Option 1: Press Enter
        search_input.send_keys(Keys.RETURN)
        # Option 2: Click search button (uncomment if required)
        # self.driver.find_element(*self.SEARCH_BUTTON).click()

    def get_search_results(self) -> List[str]:
        """
        Retrieves product titles from the search results.
        :return: List of product title strings.
        """
        elements = self.driver.find_elements(*self.PRODUCT_TITLES)
        return [el.text for el in elements if el.text.strip()]

    def validate_search_results(self, keyword: str) -> bool:
        """
        Validates that at least one product title contains the search keyword.
        :param keyword: The search keyword to validate against results.
        :return: True if matching results found, else False.
        """
        results = self.get_search_results()
        return any(keyword.lower() in title.lower() for title in results)