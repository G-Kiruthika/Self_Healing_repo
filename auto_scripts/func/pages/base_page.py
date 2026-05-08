"""Base page class with common methods for all page objects."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yaml


class BasePage:
    """Base class for all page objects.
    
    Provides common methods for interacting with web elements.
    """
    
    def __init__(self, driver):
        """Initialize BasePage with WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, self._get_explicit_wait())
    
    def _get_explicit_wait(self):
        """Get explicit wait timeout from config.
        
        Returns:
            int: Explicit wait timeout in seconds
        """
        try:
            with open('auto_scripts/func/config/config.yaml', 'r') as f:
                config = yaml.safe_load(f)
                return config.get('ui', {}).get('explicit_wait', 20)
        except:
            return 20
    
    def find_element(self, locator):
        """Find element using the provided locator.
        
        Args:
            locator (tuple): Tuple of (By, value)
            
        Returns:
            WebElement: Found web element
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Find multiple elements using the provided locator.
        
        Args:
            locator (tuple): Tuple of (By, value)
            
        Returns:
            list: List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator):
        """Click on element identified by locator.
        
        Args:
            locator (tuple): Tuple of (By, value)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text into element identified by locator.
        
        Args:
            locator (tuple): Tuple of (By, value)
            text (str): Text to enter
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from element identified by locator.
        
        Args:
            locator (tuple): Tuple of (By, value)
            
        Returns:
            str: Element text
        """
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible.
        
        Args:
            locator (tuple): Tuple of (By, value)
            timeout (int, optional): Custom timeout in seconds
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            if timeout:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(EC.visibility_of_element_located(locator))
            else:
                self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Tuple of (By, value)
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present.
        
        Args:
            locator (tuple): Tuple of (By, value)
            timeout (int, optional): Custom timeout in seconds
            
        Returns:
            WebElement: Found web element
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_to_be_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Tuple of (By, value)
            timeout (int, optional): Custom timeout in seconds
            
        Returns:
            WebElement: Clickable web element
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.element_to_be_clickable(locator))
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def get_attribute(self, locator, attribute):
        """Get attribute value from element.
        
        Args:
            locator (tuple): Tuple of (By, value)
            attribute (str): Attribute name
            
        Returns:
            str: Attribute value
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def scroll_to_element(self, locator):
        """Scroll to element.
        
        Args:
            locator (tuple): Tuple of (By, value)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def switch_to_frame(self, frame_locator):
        """Switch to iframe.
        
        Args:
            frame_locator (tuple): Tuple of (By, value) for frame
        """
        frame = self.find_element(frame_locator)
        self.driver.switch_to.frame(frame)
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe."""
        self.driver.switch_to.default_content()
    
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
        self.driver.refresh()
    
    def navigate_back(self):
        """Navigate back in browser history."""
        self.driver.back()
    
    def navigate_forward(self):
        """Navigate forward in browser history."""
        self.driver.forward()
