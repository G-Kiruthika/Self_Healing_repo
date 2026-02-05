# SecurityLogValidationPage.py
"""
SecurityLogValidationPage
------------------------
Executive Summary:
Automates inspection of application security logs for SQL injection detection and logging per TC_SCRUM96_010.

Detailed Analysis:
- Checks logs for entries of SQL injection attempts with query details and timestamp
- Ensures proper logging for security audit and traceability

Implementation Guide:
- Use find_sql_injection_log_entry() for atomic log check
- Parameterize log path for different environments

QA Report:
- Method tested for detection of injection attempts and timestamp presence
- Assertion errors provide clear diagnostics

Troubleshooting Guide:
- Missing log entries: Validate backend logging and log path

Future Considerations:
- Extend for real-time log monitoring and alerting
- Integrate with SIEM systems
"""

import re
from typing import Optional

class SecurityLogValidationPage:
    def __init__(self, log_path: str):
        self.log_path = log_path

    def find_sql_injection_log_entry(self, injection_query: str) -> Optional[str]:
        """
        Scans security log for SQL injection attempt entry.
        Args:
            injection_query (str): The attempted injection query string
        Returns:
            str: Log line if found
        Raises:
            AssertionError: If entry not found or missing timestamp
        """
        found_entry = None
        with open(self.log_path, "r", encoding="utf-8") as log_file:
            for line in log_file:
                if injection_query in line and "SQL injection" in line:
                    # Expect timestamp in format [YYYY-MM-DD HH:MM:SS]
                    if re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", line):
                        found_entry = line
                        break
        assert found_entry is not None, f"No SQL injection log entry found for query '{injection_query}' in logs."
        return found_entry
