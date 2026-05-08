"""WebDriver factory for creating and managing browser instances."""

import yaml
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def load_config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_driver():
    """Create and return a WebDriver instance based on configuration."""
    config = load_config()
    browser_config = config.get('browser', {})
    browser_type = browser_config.get('type', 'chrome').lower()
    headless = browser_config.get('headless', False)
    implicit_wait = browser_config.get('implicit_wait', 10)
    page_load_timeout = browser_config.get('page_load_timeout', 30)
    window_size = browser_config.get('window_size', '1920x1080')
    
    driver = None
    
    if browser_type == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--window-size={window_size}')
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser_type == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser_type == 'edge':
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    return driver
