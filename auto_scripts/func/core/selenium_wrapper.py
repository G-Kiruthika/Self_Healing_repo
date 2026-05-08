"""Selenium wrapper module with common WebDriver operations.

This module provides wrapper methods for common Selenium operations with
added error handling and logging.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)

logger = logging.getLogger(__name__)


class SeleniumWrapper:
    """Wrapper class for Selenium WebDriver operations."""
    
    def __init__(self, driver, timeout=10):
        """Initialize SeleniumWrapper.
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for wait operations
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present in DOM.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            WebElement: Found element
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {wait_time}s: {locator}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            WebElement: Visible element
            
        Raises:
            TimeoutException: If element not visible within timeout
        """
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time}s: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            WebElement: Clickable element
            
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.info(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {wait_time}s: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Click on element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Raises:
            ElementNotInteractableException: If element cannot be clicked
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            element.click()
            logger.info(f"Clicked element: {locator}")
        except ElementNotInteractableException:
            logger.error(f"Element not interactable: {locator}")
            raise
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            text (str): Text to enter
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            clear_first (bool): Clear field before entering text. Defaults to True.
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Entered text '{text}' into element: {locator}")
        except Exception as e:
            logger.error(f"Failed to enter text into element {locator}: {str(e)}")
            raise
    
    def get_text(self, locator, timeout=None):
        """Get text from element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            str: Element text
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            text = element.text
            logger.info(f"Got text '{text}' from element: {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator, timeout=2):
        """Check if element is visible.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int): Timeout for check. Defaults to 2.
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=2):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int): Timeout for check. Defaults to 2.
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            attribute (str): Attribute name
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            str: Attribute value
        """
        try:
            element = self.wait_for_element(locator, timeout)
            value = element.get_attribute(attribute)
            logger.info(f"Got attribute '{attribute}' = '{value}' from element: {locator}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute from element {locator}: {str(e)}")
            raise
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
        """
        try:
            element = self.wait_for_element(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.info(f"Scrolled to element: {locator}")
        except Exception as e:
            logger.error(f"Failed to scroll to element {locator}: {str(e)}")
            raise
