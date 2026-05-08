"""Driver factory module for WebDriver instantiation.

This module provides factory methods to create and configure WebDriver instances
for different browsers based on configuration.
"""

import yaml
from pathlib import Path
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


def load_config():
    """Load configuration from config.yaml file.
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_driver(browser=None, headless=False):
    """Factory method to create WebDriver instance.
    
    Args:
        browser (str, optional): Browser type ('chrome', 'firefox', 'edge'). 
                                Defaults to value from config.
        headless (bool, optional): Run browser in headless mode. Defaults to False.
    
    Returns:
        WebDriver: Configured WebDriver instance
        
    Raises:
        ValueError: If unsupported browser is specified
    """
    config = load_config()
    
    if browser is None:
        browser = config.get('ui', {}).get('browser', 'chrome').lower()
    
    if headless is False:
        headless = config.get('ui', {}).get('headless', False)
    
    implicit_wait = config.get('ui', {}).get('implicit_wait', 10)
    page_load_timeout = config.get('ui', {}).get('page_load_timeout', 30)
    
    driver = None
    
    if browser == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser == 'edge':
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox, edge")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    return driver
