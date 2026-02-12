import pytest
from core.driver_factory import get_driver


@pytest.fixture(scope="function")
def driver():
 """Fixture to provide WebDriver instance for tests.
 
 Yields:
 WebDriver: Selenium WebDriver instance
 """
 driver_instance = get_driver()
 yield driver_instance
 driver_instance.quit()


@pytest.fixture(scope="session")
def test_config():
 """Fixture to load test configuration.
 
 Returns:
 dict: Configuration dictionary
 """
 import yaml
 with open('config/config.yaml', 'r') as f:
 config = yaml.safe_load(f)
 return config
