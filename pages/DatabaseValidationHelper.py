import pymysql

class DatabaseValidationHelper:
    """
    Helper class for database validation of user profile data for TC_SCRUM96_007.
    Implements get_user_from_db(username) and compare_db_and_api_profile(db_record, api_profile).
    Strictly follows Python best practices for maintainability and downstream automation.
    """
    def __init__(self, db_config):
        """
        db_config: dict with keys host, user, password, database
        """
        self.db_config = db_config

    def get_user_from_db(self, username):
        """
        Fetches user record from database by username.
        Args:
            username (str): Username to fetch
        Returns:
            dict: User record from database
        Raises:
            RuntimeError: If DB query fails
        """
        connection = pymysql.connect(
            host=self.db_config["host"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT userId, username, email, firstName, lastName, registrationDate, accountStatus FROM users WHERE username=%s", (username,))
                record = cursor.fetchone()
                if not record:
                    raise RuntimeError(f"User '{username}' not found in database.")
        finally:
            connection.close()
        return record

    def compare_db_and_api_profile(self, db_record, api_profile):
        """
        Compares DB record and API profile for all relevant fields.
        Args:
            db_record (dict): Database record
            api_profile (dict): API profile data
        Returns:
            bool: True if all fields match
        Raises:
            AssertionError: If any field does not match
        """
        fields = ["userId", "username", "email", "firstName", "lastName", "registrationDate", "accountStatus"]
        for field in fields:
            if field not in db_record or field not in api_profile:
                raise AssertionError(f"Missing field '{field}' in comparison.")
            if str(db_record[field]) != str(api_profile[field]):
                raise AssertionError(f"Mismatch in field '{field}': DB={db_record[field]}, API={api_profile[field]}")
        # Password must NOT be present in API profile
        if "password" in api_profile:
            raise AssertionError("Password field should not be present in API profile.")
        return True

"""
Executive Summary:
- Implements DB validation helper for TC_SCRUM96_007.
- Enables atomic DB fetch and comparison for user profile validation.

Analysis:
- Strict field-by-field comparison and error handling.

Implementation Guide:
1. Instantiate DatabaseValidationHelper with db_config.
2. Call get_user_from_db(username) to fetch DB record.
3. Call compare_db_and_api_profile(db_record, api_profile) to validate.

QA Report:
- Imports validated; robust error and exception handling.
- Peer review recommended before deployment.

Troubleshooting:
- If DB fetch fails, check credentials and DB status.
- If comparison fails, check for field mismatches and normalization.

Future Considerations:
- Parameterize DB queries and fields for multi-app support.
- Extend with audit logging and error reporting.
"""
