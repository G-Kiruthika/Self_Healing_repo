"""Base page class providing common functionality for all page objects."""

from core.selenium_wrapper import SeleniumWrapper
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver):
        """Initialize BasePage.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wrapper = SeleniumWrapper(driver)
    
    def find_element(self, locator, timeout=None):
        """Find element using locator.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            WebElement: Found element
        """
        return self.wrapper.wait_for_element(locator, timeout)
    
    def click_element(self, locator, timeout=None):
        """Click element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        """
        self.wrapper.click_element(locator, timeout)
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into element.
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            timeout (int, optional): Custom timeout
            clear_first (bool): Clear field before entering text
        """
        self.wrapper.enter_text(locator, text, timeout, clear_first)
    
    def get_text(self, locator, timeout=None):
        """Get text from element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            str: Element text
        """
        return self.wrapper.get_text(locator, timeout)
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Timeout for check
        
        Returns:
            bool: True if visible, False otherwise
        """
        return self.wrapper.is_element_visible(locator, timeout)
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Timeout for check
        
        Returns:
            bool: True if present, False otherwise
        """
        return self.wrapper.is_element_present(locator, timeout)
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        """
        self.wrapper.scroll_to_element(locator, timeout)
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        """
        self.wrapper.hover_over_element(locator, timeout)
    
    def navigate_to(self, url):
        """Navigate to URL.
        
        Args:
            url (str): Target URL
        """
        self.driver.get(url)
        logger.info(f"Navigated to: {url}")
    
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
