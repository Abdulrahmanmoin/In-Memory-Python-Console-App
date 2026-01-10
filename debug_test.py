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

def debug_test():
    print("Testing basic auth functionality...")

    # Test basic token creation
    user_id = "123"
    username = "testuser"

    print(f"Creating access token for user {user_id} ({username})")
    access_token = create_access_token(user_id, username)
    print(f"Access token created: {access_token[:50]}...")

    print("Verifying access token...")
    token_data = verify_access_token(access_token)
    print(f"Token data: {token_data}")

    if token_data:
        print(f"User ID: {token_data.user_id}")
        print(f"Username: {token_data.username}")
        print(f"Token type: {token_data.token_type}")
        print(f"Expiration: {token_data.exp}")
        print(f"Issued at: {token_data.iat}")
        print("✓ Access token verification successful")
    else:
        print("✗ Access token verification failed")

    print("\nTesting refresh token...")
    refresh_token = create_refresh_token(user_id, username)
    print(f"Refresh token created: {refresh_token[:50]}...")

    refresh_token_data = verify_refresh_token(refresh_token)
    print(f"Refresh token data: {refresh_token_data}")

    if refresh_token_data:
        print(f"User ID: {refresh_token_data.user_id}")
        print(f"Username: {refresh_token_data.username}")
        print(f"Token type: {refresh_token_data.token_type}")
        print("✓ Refresh token verification successful")
    else:
        print("✗ Refresh token verification failed")

if __name__ == "__main__":
    debug_test()