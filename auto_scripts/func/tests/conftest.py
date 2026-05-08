"""
Pytest configuration file for functional automation tests.
Contains fixtures for driver setup and teardown.
"""

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import yaml
import os


@pytest.fixture(scope="function")
def driver():
    """
    Fixture to initialize and provide the Appium driver for mobile automation.
    Scope is set to 'function' so each test gets a fresh driver instance.
    
    Yields:
        webdriver: Appium WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            capabilities = config.get('appium', {})
    else:
        # Default capabilities if config doesn't exist
        capabilities = {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'deviceName': 'Android Emulator',
            'app': '/path/to/hpx.apk',
            'appPackage': 'com.hp.hpx',
            'appActivity': '.MainActivity',
            'noReset': False,
            'fullReset': False
        }
    
    # Initialize Appium driver
    options = UiAutomator2Options()
    for key, value in capabilities.items():
        options.set_capability(key, value)
    
    appium_server_url = capabilities.get('appium_server_url', 'http://localhost:4723')
    driver = webdriver.Remote(appium_server_url, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Teardown: Quit driver after test
    driver.quit()


@pytest.fixture(scope="session")
def test_config():
    """
    Fixture to load and provide test configuration data.
    Scope is set to 'session' so config is loaded once per test session.
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}
