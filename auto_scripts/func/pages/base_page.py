"""Base page module containing common page object functionality.

This module provides the BasePage class that all page objects should inherit from.
It includes common methods for element interactions and navigation.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.selenium_wrapper import SeleniumWrapper

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects.
    
    Provides common functionality for page interactions including
    element finding, waiting, clicking, and text entry.
    """
    
    def __init__(self, driver, timeout=10):
        """Initialize BasePage.
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for wait operations. Defaults to 10.
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.wrapper = SeleniumWrapper(driver, timeout)
    
    def find_element(self, locator, timeout=None):
        """Find element using locator.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            WebElement: Found element
        """
        return self.wrapper.wait_for_element(locator, timeout)
    
    def find_elements(self, locator):
        """Find multiple elements using locator.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            
        Returns:
            list: List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator, timeout=None):
        """Click on element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
        """
        self.wrapper.click_element(locator, timeout)
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            text (str): Text to enter
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            clear_first (bool): Clear field before entering text. Defaults to True.
        """
        self.wrapper.enter_text(locator, text, timeout, clear_first)
    
    def get_text(self, locator, timeout=None):
        """Get text from element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            str: Element text
        """
        return self.wrapper.get_text(locator, timeout)
    
    def is_element_visible(self, locator, timeout=2):
        """Check if element is visible.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int): Timeout for check. Defaults to 2.
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        return self.wrapper.is_element_visible(locator, timeout)
    
    def is_element_present(self, locator, timeout=2):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int): Timeout for check. Defaults to 2.
            
        Returns:
            bool: True if element is present, False otherwise
        """
        return self.wrapper.is_element_present(locator, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            WebElement: Visible element
        """
        return self.wrapper.wait_for_element_visible(locator, timeout)
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            WebElement: Clickable element
        """
        return self.wrapper.wait_for_element_clickable(locator, timeout)
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            attribute (str): Attribute name
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
            
        Returns:
            str: Attribute value
        """
        return self.wrapper.get_attribute(locator, attribute, timeout)
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element.
        
        Args:
            locator (tuple): Element locator (By.TYPE, "value")
            timeout (int, optional): Custom timeout. Defaults to self.timeout.
        """
        self.wrapper.scroll_to_element(locator, timeout)
    
    def navigate_to(self, url):
        """Navigate to URL.
        
        Args:
            url (str): URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def get_current_url(self):
        """Get current page URL.
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title.
        
        Returns:
            str: Page title
        """
        return self.driver.title
    
    def refresh_page(self):
        """Refresh current page."""
        logger.info("Refreshing page")
        self.driver.refresh()
    
    def go_back(self):
        """Navigate back in browser history."""
        logger.info("Navigating back")
        self.driver.back()
    
    def go_forward(self):
        """Navigate forward in browser history."""
        logger.info("Navigating forward")
        self.driver.forward()
