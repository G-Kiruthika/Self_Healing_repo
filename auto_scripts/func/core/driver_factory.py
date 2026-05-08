"""WebDriver factory for creating browser instances."""

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def load_config():
    """Load configuration from config.yaml.
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open('config/config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Return default config if file not found
        return {
            'browser': 'chrome',
            'headless': False,
            'implicit_wait': 10,
            'page_load_timeout': 30
        }


def get_driver(browser=None, headless=None):
    """Create and return a WebDriver instance.
    
    Args:
        browser: Browser name ('chrome', 'firefox', 'edge'). If None, uses config.
        headless: Run in headless mode. If None, uses config.
        
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    
    # Use provided values or fall back to config
    browser = browser or config.get('browser', 'chrome')
    headless = headless if headless is not None else config.get('headless', False)
    implicit_wait = config.get('implicit_wait', 10)
    page_load_timeout = config.get('page_load_timeout', 30)
    
    driver = None
    
    if browser.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    
    elif browser.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    
    elif browser.lower() == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    driver.maximize_window()
    
    return driver
