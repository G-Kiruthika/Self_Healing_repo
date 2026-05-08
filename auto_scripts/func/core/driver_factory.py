"""WebDriver factory for creating browser instances."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging

logger = logging.getLogger(__name__)


def get_driver(browser="chrome", headless=False, **kwargs):
    """Create and return a WebDriver instance.
    
    Args:
        browser (str): Browser name - chrome, firefox, edge, safari
        headless (bool): Run browser in headless mode
        **kwargs: Additional browser-specific options
    
    Returns:
        WebDriver: Selenium WebDriver instance
    
    Raises:
        ValueError: If unsupported browser is specified
    """
    browser = browser.lower()
    
    try:
        if browser == "chrome":
            return _get_chrome_driver(headless, **kwargs)
        elif browser == "firefox":
            return _get_firefox_driver(headless, **kwargs)
        elif browser == "edge":
            return _get_edge_driver(headless, **kwargs)
        elif browser == "safari":
            return _get_safari_driver(**kwargs)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    except Exception as e:
        logger.error(f"Failed to create {browser} driver: {str(e)}")
        raise


def _get_chrome_driver(headless=False, **kwargs):
    """Create Chrome WebDriver instance."""
    options = ChromeOptions()
    
    if headless:
        options.add_argument("--headless")
    
    # Common Chrome options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Add custom options from kwargs
    for key, value in kwargs.items():
        if key.startswith("chrome_"):
            options.add_argument(f"--{key[7:]}={value}")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    logger.info("Chrome driver created successfully")
    return driver


def _get_firefox_driver(headless=False, **kwargs):
    """Create Firefox WebDriver instance."""
    options = FirefoxOptions()
    
    if headless:
        options.add_argument("--headless")
    
    # Add custom options from kwargs
    for key, value in kwargs.items():
        if key.startswith("firefox_"):
            options.add_argument(f"--{key[8:]}={value}")
    
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    logger.info("Firefox driver created successfully")
    return driver


def _get_edge_driver(headless=False, **kwargs):
    """Create Edge WebDriver instance."""
    options = EdgeOptions()
    
    if headless:
        options.add_argument("--headless")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Add custom options from kwargs
    for key, value in kwargs.items():
        if key.startswith("edge_"):
            options.add_argument(f"--{key[5:]}={value}")
    
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    logger.info("Edge driver created successfully")
    return driver


def _get_safari_driver(**kwargs):
    """Create Safari WebDriver instance."""
    driver = webdriver.Safari()
    
    logger.info("Safari driver created successfully")
    return driver


def get_remote_driver(command_executor, desired_capabilities, **kwargs):
    """Create Remote WebDriver instance for Selenium Grid.
    
    Args:
        command_executor (str): Grid hub URL
        desired_capabilities (dict): Browser capabilities
        **kwargs: Additional options
    
    Returns:
        WebDriver: Remote WebDriver instance
    """
    driver = webdriver.Remote(
        command_executor=command_executor,
        desired_capabilities=desired_capabilities
    )
    
    logger.info(f"Remote driver created for {desired_capabilities.get('browserName')}")
    return driver
