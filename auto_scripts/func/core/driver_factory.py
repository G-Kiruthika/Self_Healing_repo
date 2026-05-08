"""WebDriver factory for creating and configuring browser instances."""

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
        with open('auto_scripts/func/config/config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Return default configuration if file not found
        return {
            'ui': {
                'browser': 'chrome',
                'headless': False,
                'implicit_wait': 10,
                'explicit_wait': 20,
                'page_load_timeout': 30
            }
        }


def get_driver(browser=None, headless=None):
    """Create and configure WebDriver instance.
    
    Args:
        browser (str, optional): Browser name (chrome, firefox, edge). Defaults to config value.
        headless (bool, optional): Run browser in headless mode. Defaults to config value.
        
    Returns:
        WebDriver: Configured Selenium WebDriver instance
        
    Raises:
        ValueError: If unsupported browser is specified
    """
    config = load_config()
    ui_config = config.get('ui', {})
    browser_options_config = config.get('browser_options', {})
    
    # Use provided values or fall back to config
    browser = browser or ui_config.get('browser', 'chrome')
    headless = headless if headless is not None else ui_config.get('headless', False)
    
    driver = None
    
    if browser.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        
        # Add arguments from config
        chrome_config = browser_options_config.get('chrome', {})
        for arg in chrome_config.get('arguments', []):
            options.add_argument(arg)
        
        # Add experimental options
        exp_options = chrome_config.get('experimental_options', {})
        if exp_options:
            for key, value in exp_options.items():
                options.add_experimental_option(key, value)
        
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        
        # Add arguments from config
        firefox_config = browser_options_config.get('firefox', {})
        for arg in firefox_config.get('arguments', []):
            options.add_argument(arg)
        
        # Add preferences
        prefs = firefox_config.get('preferences', {})
        for key, value in prefs.items():
            options.set_preference(key, value)
        
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser.lower() == 'edge':
        options = webdriver.EdgeOptions()
        
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox, edge")
    
    # Set timeouts
    driver.implicitly_wait(ui_config.get('implicit_wait', 10))
    driver.set_page_load_timeout(ui_config.get('page_load_timeout', 30))
    
    return driver
