"""Base page class with common UI actions and navigation methods."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver, timeout=10):
        """Initialize BasePage with driver and default timeout.
        
        Args:
            driver: WebDriver instance
            timeout: Default wait timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, locator):
        """Find and return a web element.
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            WebElement
        """
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator):
        """Click on a web element.
        
        Args:
            locator: Tuple of (By, locator_string)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text into an input field.
        
        Args:
            locator: Tuple of (By, locator_string)
            text: Text to enter
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def is_element_visible(self, locator):
        """Check if an element is visible.
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def get_text(self, locator):
        """Get text from an element.
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            str: Element text
        """
        element = self.find_element(locator)
        return element.text
    
    def open(self, url):
        """Navigate to a URL.
        
        Args:
            url: URL to navigate to
        """
        self.driver.get(url)
