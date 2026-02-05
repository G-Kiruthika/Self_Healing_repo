"""
LoginPage PageClass for Selenium automation.
Implements TC-LOGIN-012: SQL Injection prevention on login form.
All locators are mapped from Locators.json. Strictly follows Python Selenium best practices.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)

class LoginPage:
    """
    Page Object for the Login Page.
    Implements methods for TC-LOGIN-012: SQL Injection prevention.
    """

    # Locators from Locators.json
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID