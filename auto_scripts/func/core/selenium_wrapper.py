"""Selenium wrapper with common utility methods."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def wait_for_element(driver, locator, timeout=10):
    """Wait for an element to be present.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, locator_string)
        timeout: Wait timeout in seconds
        
    Returns:
        WebElement: The found element
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located(locator))


def click_element(driver, locator, timeout=10):
    """Wait for element to be clickable and click it.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, locator_string)
        timeout: Wait timeout in seconds
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable(locator))
    element.click()


def enter_text(driver, locator, text, timeout=10):
    """Wait for element and enter text.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, locator_string)
        text: Text to enter
        timeout: Wait timeout in seconds
    """
    element = wait_for_element(driver, locator, timeout)
    element.clear()
    element.send_keys(text)


def is_element_visible(driver, locator, timeout=10):
    """Check if element is visible.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, locator_string)
        timeout: Wait timeout in seconds
        
    Returns:
        bool: True if visible, False otherwise
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.visibility_of_element_located(locator))
        return True
    except TimeoutException:
        return False


def get_element_text(driver, locator, timeout=10):
    """Get text from element.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, locator_string)
        timeout: Wait timeout in seconds
        
    Returns:
        str: Element text
    """
    element = wait_for_element(driver, locator, timeout)
    return element.text
