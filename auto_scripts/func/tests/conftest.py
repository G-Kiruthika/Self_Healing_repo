"""Pytest configuration and fixtures for UI automation tests."""

import pytest
import yaml
from core.driver_factory import get_driver


@pytest.fixture(scope="function")
def driver():
    """Fixture to initialize and teardown WebDriver for each test.
    
    Yields:
        WebDriver: Selenium WebDriver instance
    """
    # Initialize driver
    driver_instance = get_driver()
    
    # Maximize window
    driver_instance.maximize_window()
    
    # Yield driver to test
    yield driver_instance
    
    # Teardown: quit driver after test
    driver_instance.quit()


@pytest.fixture(scope="session")
def config():
    """Fixture to load configuration from config.yaml.
    
    Returns:
        dict: Configuration dictionary
    """
    with open('auto_scripts/func/config/config.yaml', 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def base_url(config):
    """Fixture to provide base URL from configuration.
    
    Args:
        config: Configuration fixture
        
    Returns:
        str: Base URL for the application
    """
    return config.get('ui', {}).get('base_url', '')


def pytest_configure(config):
    """Pytest hook to add custom markers."""
    config.addinivalue_line(
        "markers", "ui: mark test as UI automation test"
    )
    config.addinivalue_line(
        "markers", "shortcuts: mark test as shortcuts functionality test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
