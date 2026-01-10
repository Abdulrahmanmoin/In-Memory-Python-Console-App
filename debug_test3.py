#!/usr/bin/env python3
"""Debug script to test auth functionality"""

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

def debug_test():
    print("Testing basic auth functionality...")

    # Test basic token creation
    user_id = "123"
    username = "testuser"

    print(f"Creating access token for user {user_id} ({username})")
    access_token = create_access_token(user_id, username)
    print(f"Access token created: {access_token[:50]}...")

    # Let's manually test the verification process
    print("\nManual verification process:")
    try:
        payload = jwt.decode(access_token, auth_service.secret_key, algorithms=[auth_service.algorithm])
        print(f"Decoded payload: {payload}")

        # Try to create TokenData object
        token_data = TokenData(**payload)
        print(f"TokenData object: {token_data}")

        # Check if token is an access token
        if token_data.token_type != "access":
            print(f"Token type mismatch: expected 'access', got '{token_data.token_type}'")
        else:
            print("Token type matches 'access'")

        # Check expiration
        import datetime
        if token_data.exp and datetime.datetime.utcnow().timestamp() > token_data.exp:
            print("Token is expired")
        else:
            print("Token is not expired")

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