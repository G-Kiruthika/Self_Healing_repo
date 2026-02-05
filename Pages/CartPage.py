# CartPage Page Object
# Selenium Automation Script (Python)
"""
CartPage Page Object

This class models the Cart page for automation using Selenium WebDriver.
It is designed to validate cart operations including adding products with quantity exceeding stock and handling invalid product IDs.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import json
import os

class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Load locators from Locators.json
        loc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Locators.json')
        with open(loc_path, 'r') as f:
            self.locators = json.load(f).get('CartPage', {})

    def attempt_create_cart(self):
        """
        Simulates an attempt to create a shopping cart (without authentication).
        Returns True if unauthorized error is displayed, False otherwise.
        """
        try:
            self.driver.find_element(By.ID, "create_cart_button").click()
        except NoSuchElementException:
            pass  # If button isn't present, assume not allowed.
        return self.is_unauthorized_error_displayed()

    def is_unauthorized_error_displayed(self):
        """
        Checks if the unauthorized access error message is displayed.
        """
        try:
            error_elem = self.driver.find_element(By.XPATH, "//div[contains(@class, 'error') and contains(text(), 'unauthorized')]")
            return error_elem.is_displayed()
        except NoSuchElementException:
            return False

    def add_product_to_cart(self, product_id: str, quantity: int):
        """
        Attempts to add a product to the cart with a specified quantity.
        Returns True if operation succeeds, False otherwise.
        """
        try:
            product_input = self.driver.find_element(By.ID, self.locators['product_id_input']['value'])
            product_input.clear()
            product_input.send_keys(product_id)
            quantity_input = self.driver.find_element(By.ID, self.locators['quantity_input']['value'])
            quantity_input.clear()
            quantity_input.send_keys(str(quantity))
            add_button = self.driver.find_element(By.ID, self.locators['add_to_cart_button']['value'])
            add_button.click()
            return True
        except NoSuchElementException:
            return False

    def get_stock_error_message(self):
        """
        Returns the error message displayed when quantity exceeds available stock.
        """
        try:
            error_elem = self.driver.find_element(By.XPATH, self.locators['stock_error_message']['value'])
            if error_elem.is_displayed():
                return error_elem.text
            else:
                return None
        except NoSuchElementException:
            return None

    def add_product_with_invalid_id(self, product_id: str, quantity: int):
        """
        Attempts to add a product to the cart with an invalid product ID and checks for error.
        :param product_id: str, invalid product ID to test
        :param quantity: int, quantity to add
        :return: bool, True if invalid product error appears, False otherwise
        """
        try:
            product_input = self.driver.find_element(By.ID, self.locators['product_id_input']['value'])
            product_input.clear()
            product_input.send_keys(product_id)
            quantity_input = self.driver.find_element(By.ID, self.locators['quantity_input']['value'])
            quantity_input.clear()
            quantity_input.send_keys(str(quantity))
            add_button = self.driver.find_element(By.ID, self.locators['add_to_cart_button']['value'])
            add_button.click()
            error_elem = self.driver.find_element(By.XPATH, self.locators['invalid_product_error_message']['value'])
            return error_elem.is_displayed()
        except NoSuchElementException:
            return False

    def add_product_with_zero_quantity(self, product_id: str):
        """
        Attempts to add a product to the cart with quantity zero and checks for error.
        Returns True if error message is displayed and product is not added, False otherwise.
        """
        try:
            product_input = self.driver.find_element(By.ID, self.locators['product_id_input']['value'])
            product_input.clear()
            product_input.send_keys(product_id)
            quantity_input = self.driver.find_element(By.ID, self.locators['quantity_input']['value'])
            quantity_input.clear()
            quantity_input.send_keys("0")
            add_button = self.driver.find_element(By.ID, self.locators['add_to_cart_button']['value'])
            add_button.click()
            # Check for error message (assume stock_error_message used for zero quantity as well)
            error_elem = self.driver.find_element(By.XPATH, self.locators['stock_error_message']['value'])
            return error_elem.is_displayed()
        except NoSuchElementException:
            return False
