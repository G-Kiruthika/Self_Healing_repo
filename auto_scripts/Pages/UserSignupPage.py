from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserSignupPage:
    """
    Page Object for the User Signup workflow.
    Provides methods to interact with the user registration process.
    """
    URL = "https://example-ecommerce.com/signup"
    USERNAME_FIELD = (By.ID, "signup-username")
    EMAIL_FIELD = (By.ID, "signup-email")
    PASSWORD_FIELD = (By.ID, "signup-password")
    SIGNUP_SUBMIT_BUTTON = (By.ID, "signup-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.signup-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.signup-error")
    EMAIL_EXISTS_MESSAGE = (By.XPATH, "//*[contains(text(), 'Email already exists')]")
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
    
    def go_to_signup_page(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
    
    def enter_username(self, username):
        username_input = self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
        username_input.clear()
        username_input.send_keys(username)
    
    def enter_email(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)
    
    def enter_password(self, password):
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)
    
    def click_signup(self):
        signup_btn = self.wait.until(EC.element_to_be_clickable(self.SIGNUP_SUBMIT_BUTTON))
        signup_btn.click()
    
    def get_success_message(self):
        try:
            success_elem = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return success_elem.text
        except:
            return None
    
    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None
    
    def get_email_exists_message(self):
        try:
            email_exists_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_EXISTS_MESSAGE))
            return email_exists_elem.text
        except:
            return None
    
    def register_user(self, username, email, password):
        """
        Complete workflow: go to signup, fill fields, submit, return result.
        """
        self.go_to_signup_page()
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        self.click_signup()
        # Check for either success or error message
        success_msg = self.get_success_message()
        if success_msg:
            return {"status": "success", "message": success_msg}
        error_msg = self.get_error_message()
        if error_msg:
            return {"status": "error", "message": error_msg}
        email_exists_msg = self.get_email_exists_message()
        if email_exists_msg:
            return {"status": "conflict", "message": email_exists_msg}
        return {"status": "unknown", "message": "No clear result returned"}
    
    def register_and_validate_duplicate(self, user1, email, pwd1, user2, pwd2):
        """
        Test workflow for TC-SCRUM-96-002:
        1. Register first user
        2. Attempt to register second user with same email
        3. Validate conflict/error message
        """
        first_result = self.register_user(user1, email, pwd1)
        assert first_result["status"] == "success", f"Expected success for first user, got {first_result}"
        second_result = self.register_user(user2, email, pwd2)
        assert second_result["status"] == "conflict", f"Expected conflict for duplicate email, got {second_result}"
        assert "Email already exists" in second_result["message"], f"Expected error message 'Email already exists', got {second_result['message']}"
        return first_result, second_result
    
    @staticmethod
    def verify_user_count_in_db(db_connection, email):
        """
        Stub for database verification. Replace with actual DB access logic.
        Usage: cursor = db_connection.cursor(); cursor.execute(query); count = cursor.fetchone()[0]
        """
        query = f"SELECT COUNT(*) FROM users WHERE email='{email}'"
        cursor = db_connection.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count
