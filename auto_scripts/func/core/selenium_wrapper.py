"""Selenium wrapper providing enhanced WebDriver functionality."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import logging

logger = logging.getLogger(__name__)


class SeleniumWrapper:
    """Wrapper class for Selenium WebDriver with enhanced functionality."""
    
    def __init__(self, driver, timeout=20):
        """Initialize SeleniumWrapper.
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for explicit waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present in DOM.
        
        Args:
            locator (tuple): Element locator (By.ID, 'element_id')
            timeout (int, optional): Custom timeout
        
        Returns:
            WebElement: Found element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            WebElement: Visible element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time} seconds: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            WebElement: Clickable element
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {wait_time} seconds: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Click on element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
        logger.info(f"Clicked element: {locator}")
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into input field.
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            timeout (int, optional): Custom timeout
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Entered text '{text}' into element: {locator}")
    
    def get_text(self, locator, timeout=None):
        """Get text from element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        text = element.text
        logger.info(f"Got text '{text}' from element: {locator}")
        return text
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Timeout for check
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            logger.info(f"Element is not visible: {locator}")
            return False
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Timeout for check
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"Element is present: {locator}")
            return True
        except TimeoutException:
            logger.info(f"Element is not present: {locator}")
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.info(f"Scrolled to element: {locator}")
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element.
        
        Args:
            locator (tuple): Element locator
            timeout (int, optional): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()
        logger.info(f"Hovered over element: {locator}")
