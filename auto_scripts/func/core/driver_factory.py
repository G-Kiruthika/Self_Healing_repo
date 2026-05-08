"""WebDriver factory for creating and managing browser instances."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import yaml
import os


def load_config():
    """Load configuration from config.yaml."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_driver(browser=None, headless=None):
    """Create and return a WebDriver instance based on configuration.
    
    Args:
        browser (str, optional): Browser type ('chrome', 'firefox', 'edge'). Defaults to config value.
        headless (bool, optional): Run browser in headless mode. Defaults to config value.
    
    Returns:
        WebDriver: Configured WebDriver instance.
    """
    config = load_config()
    ui_config = config.get('ui', {})
    
    browser = browser or ui_config.get('browser', 'chrome').lower()
    headless = headless if headless is not None else ui_config.get('headless', False)
    implicit_wait = ui_config.get('implicit_wait', 10)
    page_load_timeout = ui_config.get('page_load_timeout', 30)
    
    driver = None
    
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    driver.maximize_window()
    
    return driver
