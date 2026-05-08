"""Pytest configuration and fixtures for UI test automation."""

import pytest
import yaml
from pathlib import Path
from auto_scripts.func.core.driver_factory import get_driver


@pytest.fixture(scope="session")
def config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def driver(config):
    """Create and return WebDriver instance.
    
    Yields:
        WebDriver: Selenium WebDriver instance
    """
    browser = config.get('browser', 'chrome')
    headless = config.get('headless', False)
    
    driver_instance = get_driver(browser=browser, headless=headless)
    
    # Implicit wait
    driver_instance.implicitly_wait(config.get('implicit_wait', 10))
    
    yield driver_instance
    
    # Teardown
    driver_instance.quit()


@pytest.fixture(scope="function")
def base_url(config):
    """Return base URL from configuration."""
    return config.get('base_url', '')


def pytest_configure(config):
    """Pytest configuration hook."""
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
