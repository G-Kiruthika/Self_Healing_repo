# -*- coding: utf-8 -*-
"""
JWTUtils
--------
Executive Summary:
Utility class for decoding and validating JWT tokens using PyJWT. Ensures claims integrity and expiration checks for secure API automation.

Implementation Guide:
- Use decode_and_validate_jwt to verify JWT structure, claims, and expiration.
- Integrate with login and profile API automation for authentication validation.

QA Report:
- All validation paths are unit-tested with valid and invalid tokens.
- Robust exception handling for signature, expiration, and claim errors.

Troubleshooting:
- Signature errors: Check secret/key and algorithm match.
- Expired tokens: Confirm system time and token issuance.
- Missing claims: Validate token generation logic in backend.

Future Considerations:
- Support for additional claims and custom validations.
- Extend for JWE (encrypted JWT) support.

"""

import jwt
import datetime
from typing import Dict, Optional

class JWTUtils:
    """
    Utility class for decoding and validating JWT tokens.
    """
    @staticmethod
    def decode_and_validate_jwt(token: str, secret: Optional[str] = None, algorithms: Optional[list] = None) -> Dict:
        """
        Decodes and validates JWT token claims and expiration.
        Args:
            token (str): JWT token string.
            secret (str, optional): Secret key for decoding (if verifying signature).
            algorithms (list, optional): List of allowed algorithms (default ['HS256']).
        Returns:
            dict: Decoded JWT payload if valid.
        Raises:
            AssertionError: For missing claims or expired/invalid token.
        """
        if algorithms is None:
            algorithms = ['HS256']
        try:
            if secret:
                payload = jwt.decode(token, secret, algorithms=algorithms)
            else:
                payload = jwt.decode(token, options={"verify_signature": False}, algorithms=algorithms)
            assert 'sub' in payload, "Subject (sub) claim missing"
            assert 'exp' in payload, "Expiration (exp) claim missing"
            assert 'iat' in payload, "Issued at (iat) claim missing"
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            assert exp_time > datetime.datetime.utcnow(), "Token has expired"
            return payload
        except jwt.ExpiredSignatureError:
            raise AssertionError("Token has expired")
        except jwt.DecodeError as e:
            raise AssertionError(f"Invalid JWT token: {e}")
        except Exception as e:
            raise AssertionError(f"JWT validation failed: {e}")
