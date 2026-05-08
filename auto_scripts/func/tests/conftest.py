"""Pytest configuration and fixtures for test suite."""

import pytest
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="function")
def driver():
    """Provide WebDriver instance for tests."""
    from core.driver_factory import get_driver
    driver = get_driver()
    yield driver
    driver.quit()
