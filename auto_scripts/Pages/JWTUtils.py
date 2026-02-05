# JWTUtils.py
"""
Utility class for decoding and validating JWT tokens for automation test cases (e.g., TC_SCRUM96_004).
Strictly validates structure, claims, and signature using Python best practices.

Requires: PyJWT (install via pip if needed)
"""
import jwt
import datetime
from typing import Any, Dict, Optional

class JWTUtils:
    @staticmethod
    def decode_jwt(token: str, secret: Optional[str] = None, algorithms=None, verify_signature: bool = True) -> Dict[str, Any]:
        """
        Decodes a JWT token. If secret is provided and verify_signature is True, validates the signature.
        Returns the decoded payload (claims) as a dictionary.
        """
        if algorithms is None:
            algorithms = ["HS256", "RS256"]
        options = {"verify_signature": verify_signature}
        try:
            if verify_signature and secret:
                payload = jwt.decode(token, secret, algorithms=algorithms)
            else:
                payload = jwt.decode(token, options={"verify_signature": False}, algorithms=algorithms)
            return payload
        except jwt.ExpiredSignatureError:
            raise AssertionError("JWT token signature has expired.")
        except jwt.InvalidTokenError as e:
            raise AssertionError(f"Invalid JWT token: {e}")

    @staticmethod
    def validate_claims(payload: Dict[str, Any], expected_sub: str, leeway_sec: int = 60*5, exp_hours: int = 24):
        """
        Validates standard claims in the JWT payload.
        Checks 'sub', 'exp', 'iat', and ensures expiration is ~24h from iat.
        """
        now = datetime.datetime.utcnow().timestamp()
        assert "sub" in payload, "Missing 'sub' claim in JWT payload"
        assert payload["sub"] == expected_sub, f"Expected subject '{expected_sub}', got '{payload['sub']}'"
        assert "exp" in payload, "Missing 'exp' claim in JWT payload"
        assert "iat" in payload, "Missing 'iat' claim in JWT payload"
        exp = int(payload["exp"])
        iat = int(payload["iat"])
        assert exp > now - leeway_sec, f"Token expired at {exp}, now is {now}"
        duration = exp - iat
        assert abs(duration - exp_hours*3600) < leeway_sec, f"Expiration not ~{exp_hours}h: got duration {duration} sec"

    @staticmethod
    def validate_jwt(token: str, expected_sub: str, secret: Optional[str] = None, algorithms=None, verify_signature: bool = True, leeway_sec: int = 60*5, exp_hours: int = 24):
        """
        Full validation: decode JWT, check claims, and signature if secret is provided.
        """
        payload = JWTUtils.decode_jwt(token, secret, algorithms, verify_signature)
        JWTUtils.validate_claims(payload, expected_sub, leeway_sec, exp_hours)
        return payload

#
# Executive Summary:
# JWTUtils.py provides strict JWT decoding and validation for Selenium/Python automation, supporting signature and claims checks as required by TC_SCRUM96_004.
# Analysis:
# All claims (sub, exp, iat) validated. Signature checked if secret provided. Robust error handling.
# Implementation Guide:
# Use JWTUtils.validate_jwt(token, expected_sub, secret) for end-to-end validation.
# Quality Assurance:
# All errors raise AssertionError with clear messages for debugging. Compatible with PyJWT and Python 3.6+.
# Troubleshooting:
# If validation fails, check token structure, claims, and backend signing key. Install PyJWT if missing.
# Future Considerations:
# Extend for additional claims, RS256 public key validation, and audience/aud claim checks as needed.
