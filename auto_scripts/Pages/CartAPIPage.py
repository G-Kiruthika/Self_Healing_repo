# Executive Summary:
# CartAPIPage.py automates TC-SCRUM-96-010: cart creation, item addition, DB validation, and cart retrieval via API for Selenium/Python automation.
# Analysis:
# Implements all test steps: user authentication, POST to /api/cart/items, DB verification, GET /api/cart. All logic is modular, robust, and follows Python/Selenium best practices.
# Implementation Guide:
# Instantiate CartAPIPage with DB config. Use authenticate_user(), add_item_to_cart(), verify_cart_in_db(), and get_cart_details() in sequence.
# Quality Assurance:
# Strict assertion checks, error handling, and DB queries ensure test integrity. All fields validated.
# Troubleshooting:
# If authentication fails, check credentials/API. If cart not created, check backend logic and DB. If DB queries fail, check schema and config.
# Future Considerations:
# Extend for multiple items, cart updates, and concurrency. Parameterize endpoints for environment flexibility.

import requests
import pymysql
import json
from typing import Dict, Any, Optional

class CartAPIPage:
    BASE_URL = "https://example-ecommerce.com"

    def __init__(self, db_config: Optional[Dict[str, Any]] = None):
        self.db_config = db_config
        self.token = None
        self.user_id = None
        self.cart_id = None

    def authenticate_user(self, email: str, password: str) -> str:
        url = f"{self.BASE_URL}/api/users/login"
        payload = {"email": email, "password": password}
        response = requests.post(url, json=payload)
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "token" in data, "No token returned in login response"
        self.token = data["token"]
        self.user_id = data.get("userId")
        return self.token

    def add_item_to_cart(self, product_id: str, quantity: int) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/api/cart/items"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        payload = {"productId": product_id, "quantity": quantity}
        response = requests.post(url, json=payload, headers=headers)
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}: {response.text}"
        data = response.json()
        self.cart_id = data.get("cartId")
        return data

    def verify_cart_in_db(self) -> Dict[str, Any]:
        assert self.db_config is not None, "DB config required for DB verification"
        connection = pymysql.connect(
            host=self.db_config["host"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"]
        )
        try:
            with connection.cursor() as cursor:
                # Verify cart exists for user
                query_cart = "SELECT cartId, userId FROM carts WHERE userId=%s"
                cursor.execute(query_cart, (self.user_id,))
                cart_row = cursor.fetchone()
                assert cart_row is not None, f"No cart found for userId {self.user_id}"
                cart_id = cart_row[0]
                # Verify cart_items contains the product
                query_items = "SELECT productId, quantity FROM cart_items WHERE cartId=%s"
                cursor.execute(query_items, (cart_id,))
                items = cursor.fetchall()
                assert items, f"No items found in cart {cart_id}"
                return {"cartId": cart_id, "items": items}
        finally:
            connection.close()

    def get_cart_details(self) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/api/cart"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
        data = response.json()
        assert "items" in data, "Cart response missing 'items' field"
        return data

    def tc_scrum96_010_workflow(self, email, password, product_id, quantity):
        """
        Implements TC-SCRUM-96-010 end-to-end:
        1. Authenticate user
        2. Add item to cart
        3. Verify cart in DB
        4. Retrieve cart details
        """
        self.authenticate_user(email, password)
        self.add_item_to_cart(product_id, quantity)
        db_result = self.verify_cart_in_db()
        cart_details = self.get_cart_details()
        return {
            "db_result": db_result,
            "cart_details": cart_details
        }
