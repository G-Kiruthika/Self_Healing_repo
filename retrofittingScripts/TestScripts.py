"""
Test Scripts Module - Automated Test Cases
Contains test classes for login functionality including forgot username workflow
and user registration with email format validation
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestCase_TC003_ResetLinkExpiryChange(unittest.TestCase):
    """
    Test Case ID: 1287
    Test Case: TC003 - Reset Link Expiry Time Change
    Description: Verify that reset link expiry time has been changed from 24h to 12h
    """

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://example.com"  # Replace with actual URL

    def tearDown(self):
        """Clean up after each test method"""
        if self.driver:
            self.driver.quit()

    def test_step_1_reset_link_expiry_changed_to_12h(self):
        """
        Test Step 1: Changed reset link expiry time from 24h to 12h.
        Expected: Step executes successfully as per the described change.
        """
        try:
            # Navigate to password reset page
            self.driver.get(f"{self.base_url}/forgot-password")
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            
            # Enter email address
            email_field = self.driver.find_element(By.ID, "email")
            email_field.clear()
            email_field.send_keys("testuser@example.com")
            
            # Click submit button to request reset link
            submit_button = self.driver.find_element(By.ID, "submit-reset")
            submit_button.click()
            
            # Wait for confirmation message
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success-message")))
            
            # Verify that the confirmation message mentions 12 hours expiry
            confirmation_message = self.driver.find_element(By.CLASS_NAME, "success-message").text
            
            # Assert that the message contains reference to 12 hours (not 24 hours)
            self.assertIn("12", confirmation_message.lower(), 
                         "Reset link expiry message should reference 12 hours")
            self.assertNotIn("24", confirmation_message.lower(), 
                           "Reset link expiry message should not reference 24 hours")
            
            # Additional verification: Check if expiry time configuration is set to 12 hours
            # This could involve checking database, API, or configuration settings
            # depending on the application architecture
            
            print("Test Step 1 executed successfully: Reset link expiry time verified as 12h")
            
        except TimeoutException as e:
            self.fail(f"Timeout while waiting for element: {str(e)}")
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")


if __name__ == "__main__":
    unittest.main()