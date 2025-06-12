"""
Firebase Authentication tools for MCP server.
"""
import asyncio
from typing import Dict, Optional
from firebase_admin import auth
from ..firebase_init import get_auth


async def verify_id_token(token: str) -> dict:
    """
    Verify a Firebase ID token and return the decoded token.

    Args:
        token: The Firebase ID token to verify

    Returns:
        dict: Decoded token information including uid, email, etc.
    """
    def _verify():
        auth_client = get_auth()
        return auth_client.verify_id_token(token)

    decoded_token = await asyncio.to_thread(_verify)
    return dict(decoded_token)


async def create_custom_token(uid: str, claims: Optional[dict] = None) -> str:
    """
    Create a custom Firebase authentication token.

    Args:
        uid: The user ID for the token
        claims: Optional custom claims to include in the token

    Returns:
        str: The custom token string
    """
    def _create():
        auth_client = get_auth()
        return auth_client.create_custom_token(uid, claims)

    token = await asyncio.to_thread(_create)
    return token.decode('utf-8')


async def get_user(uid: str) -> dict:
    """
    Get user information by UID.

    Args:
        uid: The user ID to look up

    Returns:
        dict: User information including email, display_name, etc.
    """
    def _get():
        auth_client = get_auth()
        user = auth_client.get_user(uid)
        return {
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name,
            'phone_number': user.phone_number,
            'photo_url': user.photo_url,
            'disabled': user.disabled,
            'email_verified': user.email_verified,
            'provider_data': [
                {
                    'uid': provider.uid,
                    'email': provider.email,
                    'display_name': provider.display_name,
                    'photo_url': provider.photo_url,
                    'provider_id': provider.provider_id
                }
                for provider in user.provider_data
            ]
        }

    return await asyncio.to_thread(_get)


async def delete_user(uid: str) -> bool:
    """
    Delete a user by UID.

    Args:
        uid: The user ID to delete

    Returns:
        bool: True if successful
    """
    def _delete():
        auth_client = get_auth()
        auth_client.delete_user(uid)
        return True

    return await asyncio.to_thread(_delete)
