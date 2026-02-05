# ProductDatabaseIntegrityPage.py
"""
ProductDatabaseIntegrityPage
---------------------------
Executive Summary:
Automates verification of database integrity after product operations, ensuring no unauthorized data exposure or modification for TC_SCRUM96_010.

Detailed Analysis:
- Checks that products table contains only legitimate test data
- Validates against unauthorized access or tampering

Implementation Guide:
- Use verify_products_table_integrity() for atomic DB check
- Integrate with pipeline for post-operation validation

QA Report:
- Method tested for edge cases and tampering scenarios
- Clear assertion errors and diagnostic output

Troubleshooting Guide:
- Integrity failures: Check test data setup, DB triggers, and user privileges

Future Considerations:
- Extend for audit log checks and role-based access validation
- Parameterize for multi-tenant DBs
"""

import pymysql
from typing import Dict, Any, List

class ProductDatabaseIntegrityPage:
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config

    def verify_products_table_integrity(self, expected_products: List[Dict[str, Any]]) -> None:
        """
        Verifies products table contains only expected test data.
        Args:
            expected_products (list): List of expected product dicts
        Raises:
            AssertionError: If unexpected products found
        """
        conn = pymysql.connect(**self.db_config)
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT name, description, price FROM products")
                db_products = cursor.fetchall()
                expected_set = set((p["name"], p["description"], float(p["price"])) for p in expected_products)
                db_set = set((p["name"], p["description"], float(p["price"])) for p in db_products)
                assert db_set <= expected_set, f"Database contains unexpected products: {db_set - expected_set}"
        finally:
            conn.close()
        print("Product database integrity verified.")
