"""Selenium wrapper with common WebDriver operations."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumWrapper:
    """Wrapper class for common Selenium operations."""
    
    def __init__(self, driver, timeout=10):
        """Initialize SeleniumWrapper with driver and timeout.
        
        Args:
            driver: WebDriver instance
            timeout: Default timeout for wait operations
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present and visible.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
            
        Returns:
            WebElement if found
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
            
        Returns:
            WebElement if found and clickable
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator, timeout=None):
        """Click on an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def enter_text(self, locator, text, timeout=None):
        """Enter text into an input field.
        
        Args:
            locator: Tuple of (By, value)
            text: Text to enter
            timeout: Optional timeout override
        """
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """Get text from an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
            
        Returns:
            Text content of element
        """
        element = self.wait_for_element(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
            
        Returns:
            True if visible, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout if timeout else 5)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_present(self, locator):
        """Check if element is present in DOM.
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            True if present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over an element.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        """
        element = self.wait_for_element(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from an element.
        
        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name
            timeout: Optional timeout override
            
        Returns:
            Attribute value
        """
        element = self.wait_for_element(locator, timeout)
        return element.get_attribute(attribute)
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain specific fragment.
        
        Args:
            url_fragment: URL fragment to wait for
            timeout: Optional timeout override
            
        Returns:
            True if URL contains fragment
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.url_contains(url_fragment))
