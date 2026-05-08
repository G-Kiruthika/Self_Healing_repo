"""Selenium wrapper with enhanced wait and interaction methods."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
import logging

logger = logging.getLogger(__name__)


class SeleniumWrapper:
    """Wrapper class for Selenium WebDriver operations."""

    def __init__(self, driver, timeout=20):
        """Initialize SeleniumWrapper.
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, locator, timeout=None, condition="presence"):
        """Wait for element with specified condition.
        
        Args:
            locator (tuple): Element locator (By.*, value)
            timeout (int): Wait timeout (uses default if None)
            condition (str): Wait condition - presence, visible, clickable
        
        Returns:
            WebElement: Found element
        
        Raises:
            TimeoutException: If element not found within timeout
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        
        conditions = {
            "presence": EC.presence_of_element_located,
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable
        }
        
        try:
            condition_func = conditions.get(condition, EC.presence_of_element_located)
            element = wait.until(condition_func(locator))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {timeout}s: {locator}")
            raise

    def click_element(self, locator, timeout=None):
        """Click on element with wait.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        
        Returns:
            bool: True if click successful
        """
        try:
            element = self.wait_for_element(locator, timeout, "clickable")
            element.click()
            logger.debug(f"Clicked element: {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
            raise

    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """Enter text into element.
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            timeout (int): Wait timeout
            clear_first (bool): Clear field before entering text
        
        Returns:
            bool: True if text entered successfully
        """
        try:
            element = self.wait_for_element(locator, timeout, "visible")
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.debug(f"Entered text '{text}' into element: {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to enter text into {locator}: {str(e)}")
            raise

    def get_text(self, locator, timeout=None):
        """Get text from element.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        
        Returns:
            str: Element text
        """
        try:
            element = self.wait_for_element(locator, timeout, "visible")
            text = element.text
            logger.debug(f"Got text '{text}' from element: {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {locator}: {str(e)}")
            raise

    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        
        Returns:
            bool: True if element is visible
        """
        try:
            self.wait_for_element(locator, timeout, "visible")
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        
        Returns:
            bool: True if element is present
        """
        try:
            self.wait_for_element(locator, timeout, "presence")
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear from DOM.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        
        Returns:
            bool: True if element disappeared
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        
        try:
            wait.until(EC.invisibility_of_element_located(locator))
            logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Element still visible after {timeout}s: {locator}")
            return False

    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element.
        
        Args:
            locator (tuple): Element locator
            attribute (str): Attribute name
            timeout (int): Wait timeout
        
        Returns:
            str: Attribute value
        """
        try:
            element = self.wait_for_element(locator, timeout)
            value = element.get_attribute(attribute)
            logger.debug(f"Got attribute '{attribute}'='{value}' from {locator}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute from {locator}: {str(e)}")
            raise

    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout
        
        Returns:
            bool: True if scrolled successfully
        """
        try:
            element = self.wait_for_element(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.debug(f"Scrolled to element: {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to scroll to {locator}: {str(e)}")
            raise
