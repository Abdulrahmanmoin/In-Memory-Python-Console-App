#!/usr/bin/env python3
"""Debug script to test auth functionality with time check"""

import os
import sys
sys.path.insert(0, '/mnt/d/todo_phase1')

from backend.src.services.auth import (
    auth_service,
    create_access_token,
    verify_access_token,
    create_refresh_token,
    verify_refresh_token,
    refresh_access_token
)
from jose import jwt, JWTError
from backend.src.services.auth import TokenData, RefreshTokenData
import base64
import json
import datetime

def decode_token_payload(token: str):
    """Decode JWT without verification to see the payload"""
    try:
        # Split the token
        parts = token.split('.')
        if len(parts) != 3:
            return None

        # Decode the payload (second part)
        payload = parts[1]
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        decoded_payload = base64.urlsafe_b64decode(payload)
        return json.loads(decoded_payload)
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None

def debug_test():
    print("Testing basic auth functionality...")

    # Check current time
    current_time = datetime.datetime.utcnow().timestamp()
    print(f"Current time (UTC): {current_time}")
    print(f"Current time readable: {datetime.datetime.fromtimestamp(current_time)}")

    # Test basic token creation
    user_id = "123"
    username = "testuser"

    print(f"\nCreating access token for user {user_id} ({username})")
    access_token = create_access_token(user_id, username)
    print(f"Access token created: {access_token[:50]}...")

    # Decode the payload to see what's in it
    payload = decode_token_payload(access_token)
    print(f"Access token payload: {payload}")

    if payload:
        print(f"  Expiration time: {payload['exp']}")
        print(f"  Expiration readable: {datetime.datetime.fromtimestamp(payload['exp'])}")
        print(f"  Time until expiration: {payload['exp'] - current_time} seconds")
        print(f"  Is expired: {current_time > payload['exp']}")

    print("\nManual verification process:")
    try:
        # Verify with the auth service's secret and algorithm
        decoded_payload = jwt.decode(access_token, auth_service.secret_key, algorithms=[auth_service.algorithm])
        print(f"Decoded payload: {decoded_payload}")

        # Try to create TokenData object
        token_data = TokenData(**decoded_payload)
        print(f"TokenData object: {token_data}")

        # Check if token is an access token
        if token_data.token_type != "access":
            print(f"Token type mismatch: expected 'access', got '{token_data.token_type}'")
        else:
            print("Token type matches 'access'")

        # Check expiration using current time
        if token_data.exp and current_time > token_data.exp:
            print(f"Token is expired: {current_time} > {token_data.exp}")
        else:
            print(f"Token is not expired: {current_time} <= {token_data.exp}")

    except JWTError as e:
        print(f"JWTError: {e}")
    except Exception as e:
        print(f"Other error: {e}")
        import traceback
        traceback.print_exc()

    print("\nUsing auth service verify method:")
    token_data = verify_access_token(access_token)
    print(f"Service verification result: {token_data}")

if __name__ == "__main__":
    debug_test()