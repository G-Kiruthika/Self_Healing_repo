"""
TC_SCRUM96_004OrchestratorPage.py

Executive Summary:
------------------
This PageClass automates the end-to-end workflow for test case TC_SCRUM96_004: user registration, login, JWT validation, and protected profile API access. It orchestrates existing atomic PageClasses, ensuring strict code integrity, robust error handling, and structured output for downstream automation.

Analysis:
---------
- Step 1: User registration via UserRegistrationAPIPage
- Step 2: Login and token validation via LoginPage
- Step 3: JWT structure/claims validation via JWTUtils
- Step 4: Protected endpoint access and user profile validation via ProfilePage
- All acceptance criteria are strictly validated
- Output is a dict with stepwise results and final pass/fail

Implementation Guide:
---------------------
1. Instantiate TC_SCRUM96_004OrchestratorPage
2. Call run_tc_scrum96_004(user_data) with required test data
3. Validate returned dict for stepwise results
4. Integrate into CI/CD or downstream pipeline as needed

Quality Assurance Report:
------------------------
- All imports validated
- Exception handling ensures atomic failure reporting
- Output structure matches project and downstream requirements
- Peer review and static analysis recommended before deployment

Troubleshooting Guide:
----------------------
- If registration fails: check payload and endpoint status
- If login fails: validate credentials and endpoint
- If JWT validation fails: check token structure, claims, and backend signing key
- If profile API fails: check JWT validity and endpoint

Future Considerations:
----------------------
- Parameterize endpoints for multi-environment support
- Extend for multi-user scenarios
- Integrate with test reporting frameworks for automated QA
- Add retry logic and audit reporting
"""

import requests
from auto_scripts.Pages.UserRegistrationAPIPage import UserRegistrationAPIPage
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.JWTUtils import JWTUtils
from auto_scripts.Pages.ProfilePage import ProfilePage

class TC_SCRUM96_004OrchestratorPage:
    """
    Orchestrator for TC_SCRUM96_004: User registration, login, JWT validation, and profile API access.
    """
    def __init__(self):
        self.user_registration_api = UserRegistrationAPIPage()
        self.login_page = LoginPage()
        self.jwt_utils = JWTUtils()
        self.profile_page = ProfilePage()

    def run_tc_scrum96_004(self, user_data):
        """
        Executes TC_SCRUM96_004 end-to-end and returns structured results.
        Args:
            user_data (dict): {"username", "email", "password", "firstName", "lastName"}
        Returns:
            dict: Stepwise results and validation messages
        """
        results = {}
        try:
            # Step 1: Register user
            reg_result = self.user_registration_api.tc_scrum96_004_register_user_and_get_jwt(user_data)
            results["step_1_registration_status_code"] = reg_result["status_code"]
            results["step_1_registration_response"] = reg_result["response"]
            results["step_1_jwt_token"] = reg_result["jwt_token"]
            results["step_1_pass"] = reg_result["status_code"] in [200, 201]
        except Exception as e:
            results["step_1_pass"] = False
            results["step_1_error"] = str(e)
            results["overall_pass"] = False
            return results
        try:
            # Step 2: Login and validate tokens
            login_result = self.login_page.tc_scrum96_004_login_and_validate_tokens(
                user_data["username"], user_data["password"], user_data["email"])
            results["step_2_login_status_code"] = login_result["status_code"]
            results["step_2_jwt_token"] = login_result["jwt_token"]
            results["step_2_refresh_token"] = login_result["refresh_token"]
            results["step_2_token_type"] = login_result["token_type"]
            results["step_2_user_details"] = login_result["user_details"]
            results["step_2_pass"] = login_result["status_code"] == 200 and login_result["token_type"].lower() == "bearer"
        except Exception as e:
            results["step_2_pass"] = False
            results["step_2_error"] = str(e)
            results["overall_pass"] = False
            return results
        try:
            # Step 3: JWT decode and validate claims
            jwt_token = results["step_2_jwt_token"]
            jwt_payload = self.jwt_utils.decode_jwt(jwt_token, verify_signature=False)
            self.jwt_utils.validate_claims(jwt_payload, user_data["username"], exp_hours=24)
            results["step_3_jwt_payload"] = jwt_payload
            results["step_3_pass"] = True
        except Exception as e:
            results["step_3_pass"] = False
            results["step_3_error"] = str(e)
            results["overall_pass"] = False
            return results
        try:
            # Step 4: Access protected profile endpoint
            profile_result = self.profile_page.tc_scrum96_004_get_profile_and_validate(
                jwt_token, user_data["username"], user_data["email"])
            results["step_4_profile_status_code"] = profile_result["status_code"]
            results["step_4_profile_data"] = profile_result["profile_data"]
            results["step_4_pass"] = profile_result["status_code"] == 200 and \
                profile_result["profile_data"]["username"] == user_data["username"] and \
                profile_result["profile_data"]["email"] == user_data["email"]
        except Exception as e:
            results["step_4_pass"] = False
            results["step_4_error"] = str(e)
            results["overall_pass"] = False
            return results
        results["overall_pass"] = all([
            results.get("step_1_pass"),
            results.get("step_2_pass"),
            results.get("step_3_pass"),
            results.get("step_4_pass")
        ])
        return results

"""
Comprehensive Documentation:
- TC_SCRUM96_004OrchestratorPage.run_tc_scrum96_004(user_data):
    - Step 1: Registers user and obtains JWT
    - Step 2: Logs in and validates tokens/user details
    - Step 3: Decodes JWT and validates claims
    - Step 4: Accesses protected profile endpoint and validates user data
    - Returns dict with stepwise results and overall pass/fail

QA Report:
- All imports validated; references existing atomic PageClasses
- Exception handling ensures atomic failure reporting
- Output structure matches downstream requirements
- Peer review and static analysis recommended before deployment

Troubleshooting:
- If any step fails, returned dict contains error message for that step
- Validate endpoints, payloads, and backend logic for failures
- Check JWT signing key and claims for token validation errors

Future Considerations:
- Parameterize endpoints for multi-environment support
- Extend for multi-user scenarios
- Integrate with test reporting frameworks for automated QA
- Add retry logic and audit reporting
"""
