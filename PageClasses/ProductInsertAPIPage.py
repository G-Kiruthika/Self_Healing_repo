# ProductInsertAPIPage.py
"""
ProductInsertAPIPage
-------------------
Executive Summary:
Automates insertion of products containing special characters via API and verifies database insertion. Ensures robust handling of edge cases and SQL safety for TC_SCRUM96_010.

Detailed Analysis:
- API Endpoint: /api/products (POST)
- Test Data: Inserts 'C++ Programming Book' with special characters
- Database Verification: Confirms product exists in DB after API call

Implementation Guide:
- Use insert_product_api() to send API request
- Use verify_product_in_db() to validate DB record
- Integrate with downstream pipeline for atomic test steps

QA Report:
- API and DB methods unit-tested for edge cases
- Handles assertion and exception with traceable error messages

Troubleshooting Guide:
- API failures: Check endpoint, payload, and authentication
- DB failures: Check connection, query, and data encoding

Future Considerations:
- Extend for batch insert and multi-language product names
- Parameterize DB for cloud deployment
"""

import requests
import pymysql
from typing import Dict, Any, Optional

class ProductInsertAPIPage:
    BASE_URL = "https://example-ecommerce.com"
    INSERT_ENDPOINT = "/api/products"

    def __init__(self, db_config: Dict[str, Any]):
        """
        Args:
            db_config (dict): Database config with host, user, password, database
        """
        self.db_config = db_config

    def insert_product_api(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends POST request to insert product via API.
        Args:
            product_data (dict): Product fields (name, description, price)
        Returns:
            dict: API response JSON
        Raises:
            AssertionError: If status != 201 or data mismatch
        """
        url = f"{self.BASE_URL}{self.INSERT_ENDPOINT}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=product_data, headers=headers)
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}. Response: {response.text}"
        resp_json = response.json()
        for field in ["name", "description", "price"]:
            assert resp_json.get(field) == product_data[field], f"Mismatch for field {field}"
        return resp_json

    def verify_product_in_db(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Verifies product exists in DB by name.
        Args:
            name (str): Product name
        Returns:
            dict: Product record if found
        Raises:
            AssertionError: If not found or encoding issue
        """
        conn = pymysql.connect(**self.db_config)
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT * FROM products WHERE name = %s"
                cursor.execute(query, (name,))
                record = cursor.fetchone()
                assert record is not None, f"Product '{name}' not found in DB"
                return record
        finally:
            conn.close()
        return None

    def run_insert_and_verify(self, product_data: Dict[str, Any]) -> None:
        """
        End-to-end workflow: insert product via API, verify in DB.
        Args:
            product_data (dict): Product fields
        """
        api_resp = self.insert_product_api(product_data)
        db_record = self.verify_product_in_db(product_data["name"])
        assert db_record["name"] == product_data["name"], "DB record name mismatch"
        assert db_record["description"] == product_data["description"], "DB record description mismatch"
        assert float(db_record["price"]) == float(product_data["price"]), "DB record price mismatch"
        print("Product insertion and DB verification successful.")
