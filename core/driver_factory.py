"""
Driver Factory Module
Provides WebDriver instantiation and management
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import yaml
import os


def get_driver(browser=None):
    """
    Get WebDriver instance based on configuration
    
    Args:
        browser (str): Browser type (chrome, firefox, edge). If None, reads from config.
        
    Returns:
        WebDriver: Configured WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            browser = browser or config.get('ui', {}).get('browser', 'chrome')
            headless = config.get('ui', {}).get('headless', False)
            implicit_wait = config.get('ui', {}).get('implicit_wait', 10)
    else:
        browser = browser or 'chrome'
        headless = False
        implicit_wait = 10
    
    driver = None
    
    if browser.lower() == 'chrome':
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=chrome_options)
        
    elif browser.lower() == 'firefox':
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
        
    elif browser.lower() == 'edge':
        edge_options = EdgeOptions()
        if headless:
            edge_options.add_argument('--headless')
        driver = webdriver.Edge(options=edge_options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.implicitly_wait(implicit_wait)
    driver.maximize_window()
    
    return driver