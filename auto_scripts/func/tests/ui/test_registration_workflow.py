# tests/ui/test_registration_workflow.py

from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver


def test_registration_valid_user():
    """
    Test Case: TC-001 - Registration Workflow
    Description: Verify user can successfully register with valid credentials
    Steps:
        1. Navigate to registration page
        2. Enter valid email, password, and name
        3. Submit registration form
        4. Verify account creation and success message
    Test Data:
        - email: user@example.com
        - password: SecurePass123
        - name: John Doe
    """
    # Initialize driver and page object
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    try:
        # Step 1: Navigate to registration page
        registration_page.go_to_registration_page()
        
        # Step 2: Enter valid registration details
        registration_page.enter_registration_details("user@example.com", "SecurePass123", "John Doe")
        
        # Step 3: Submit registration form
        registration_page.submit_registration()
        
        # Step 4: Verify account creation and success message
        registration_page.verify_registration_success()
        
    finally:
        # Cleanup
        driver.quit()
