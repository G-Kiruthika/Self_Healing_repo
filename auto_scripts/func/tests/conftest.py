"""Pytest configuration and fixtures."""

import pytest
from core.driver_factory import get_driver
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance for each test.
    
    Yields:
        WebDriver: Configured WebDriver instance
    """
    driver_instance = get_driver()
    logger.info("WebDriver instance created")
    
    yield driver_instance
    
    driver_instance.quit()
    logger.info("WebDriver instance closed")


@pytest.fixture(scope="session")
def test_config():
    """Fixture to provide test configuration.
    
    Returns:
        dict: Test configuration
    """
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test execution results."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if report.failed:
            logger.error(f"Test FAILED: {item.nodeid}")
        elif report.passed:
            logger.info(f"Test PASSED: {item.nodeid}")


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    logger.info("Pytest configuration completed")
