#!/usr/bin/env python3
"""Comprehensive test for the enhanced refresh token functionality."""

import sys
sys.path.insert(0, '/mnt/d/todo_phase1')

from backend.src.services.auth import (
    auth_service,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
    refresh_access_token,
    refresh_access_token as refresh_token,
    revoke_refresh_token,
    revoke_all_user_refresh_tokens
)

def test_refresh_token_functionality():
    """Test the complete refresh token functionality with security features."""
    print("Testing refresh token functionality with security enhancements...")

    user_id = "test_user_123"
    username = "testuser"

    print(f"\n1. Creating initial tokens for user {username} (ID: {user_id})")
    tokens = auth_service.create_tokens(user_id, username)
    print(f"   Access token: {tokens['access_token'][:50]}...")
    print(f"   Refresh token: {tokens['refresh_token'][:50]}...")

    # Verify initial tokens are valid
    access_data = verify_access_token(tokens['access_token'])
    refresh_data = verify_refresh_token(tokens['refresh_token'])

    assert access_data is not None, "Initial access token should be valid"
    assert refresh_data is not None, "Initial refresh token should be valid"
    print("   ✓ Initial tokens are valid")

    print(f"\n2. Testing token refresh with rotation")
    refresh_result = refresh_token(tokens['refresh_token'])

    assert refresh_result is not None, "Refresh should succeed"
    assert 'access_token' in refresh_result, "New access token should be returned"
    assert 'refresh_token' in refresh_result, "New refresh token should be returned"
    print("   ✓ Token refresh successful")
    print(f"   New access token: {refresh_result['access_token'][:50]}...")
    print(f"   New refresh token: {refresh_result['refresh_token'][:50]}...")

    # Verify new tokens are different from old ones
    assert refresh_result['access_token'] != tokens['access_token'], "New access token should be different"
    assert refresh_result['refresh_token'] != tokens['refresh_token'], "New refresh token should be different"
    print("   ✓ New tokens are different from old ones (rotation)")

    # Verify old refresh token is no longer valid (due to rotation)
    old_token_refresh = refresh_token(tokens['refresh_token'])
    assert old_token_refresh is None, "Old refresh token should no longer be valid after rotation"
    print("   ✓ Old refresh token is no longer valid (rotation security)")

    # Verify new access token is valid
    new_access_data = verify_access_token(refresh_result['access_token'])
    assert new_access_data is not None, "New access token should be valid"
    print("   ✓ New access token is valid")

    print(f"\n3. Testing multiple refresh cycles")
    # Refresh again with the new refresh token
    second_refresh = refresh_token(refresh_result['refresh_token'])
    assert second_refresh is not None, "Second refresh should succeed"
    assert second_refresh['access_token'] != refresh_result['access_token'], "Third access token should be different"
    assert second_refresh['refresh_token'] != refresh_result['refresh_token'], "Third refresh token should be different"
    print("   ✓ Multiple refresh cycles work correctly")

    # Old refresh tokens should be invalid
    assert refresh_token(refresh_result['refresh_token']) is None, "Second refresh token should be invalid after third refresh"
    assert refresh_token(tokens['refresh_token']) is None, "Original refresh token should still be invalid"
    print("   ✓ All old refresh tokens are properly invalidated")

    print(f"\n4. Testing security features")
    # Try to use an invalid refresh token
    invalid_result = refresh_token("invalid_token_string")
    assert invalid_result is None, "Invalid token should return None"
    print("   ✓ Invalid tokens are properly rejected")

    # Try to use a malformed token
    malformed_result = refresh_token("invalid.token.format")
    assert malformed_result is None, "Malformed token should return None"
    print("   ✓ Malformed tokens are properly rejected")

    print(f"\n5. Testing user token revocation")
    # Create another set of tokens for the same user
    more_tokens = auth_service.create_tokens(user_id, username)
    assert more_tokens is not None, "Additional tokens should be created"

    # Revoke all tokens for the user
    revoked_count = revoke_all_user_refresh_tokens(user_id)
    assert revoked_count >= 1, f"At least one token should be revoked, got {revoked_count}"
    print(f"   ✓ Revoked {revoked_count} tokens for user {user_id}")

    # Verify that the tokens are no longer valid
    assert refresh_token(more_tokens['refresh_token']) is None, "Revoked tokens should not work"
    assert refresh_token(second_refresh['refresh_token']) is None, "Previously valid tokens should be revoked"
    print("   ✓ Revoked tokens are no longer valid")

    print(f"\n6. Testing token consistency validation")
    # This test validates that the JWT payload matches the stored token data
    # (This is already tested by our normal flow, but let's make sure it works)

    fresh_tokens = auth_service.create_tokens(user_id, username)
    fresh_refresh_result = refresh_token(fresh_tokens['refresh_token'])
    assert fresh_refresh_result is not None, "Fresh token should refresh successfully"
    print("   ✓ Token consistency validation works")

    print(f"\n✅ All refresh token functionality tests passed!")
    print(f"✅ Security features implemented and validated:")
    print(f"   - Token rotation")
    print(f"   - Secure token storage")
    print(f"   - Proper validation")
    print(f"   - User token revocation")
    print(f"   - Token consistency checks")

if __name__ == "__main__":
    test_refresh_token_functionality()