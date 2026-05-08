"""Pytest configuration file for test fixtures and hooks.

This file contains shared fixtures and configuration for all tests.
"""

import pytest
import yaml
from pathlib import Path
from core.driver_factory import get_driver


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance for each test.
    
    Yields:
        WebDriver: Selenium WebDriver instance
    """
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def config():
    """Fixture to load configuration from config.yaml.
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def base_url(config):
    """Fixture to provide base URL from configuration.
    
    Args:
        config: Configuration fixture
        
    Returns:
        str: Base URL for the application
    """
    return config.get('ui', {}).get('base_url', '')


def pytest_configure(config):
    """Pytest hook for initial configuration."""
    config.addinivalue_line(
        "markers", "ui: mark test as UI automation test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
