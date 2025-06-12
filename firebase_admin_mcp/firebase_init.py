"""
Firebase Admin SDK initialization for MCP server.
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from django.conf import settings

# Global variables to hold initialized services
_db = None
_auth_client = None
_bucket = None
_initialized = False


def _initialize_firebase():
    """Initialize Firebase Admin SDK once."""
    global _db, _auth_client, _bucket, _initialized

    if _initialized:
        return

    # Initialize Firebase Admin SDK once
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(settings.SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Failed to initialize Firebase Admin SDK: {e}")
            raise

    # Initialize Firestore
    if settings.ENABLE_FIRESTORE:
        _db = firestore.client()

    # Initialize Auth
    if settings.ENABLE_AUTH:
        _auth_client = auth

    # Initialize Storage
    if settings.ENABLE_STORAGE and settings.FIREBASE_STORAGE_BUCKET:
        try:
            _bucket = storage.bucket(settings.FIREBASE_STORAGE_BUCKET)
        except Exception as e:
            print(f"Failed to initialize Storage bucket: {e}")
            _bucket = None

    _initialized = True


def get_db():
    """Get Firestore database client."""
    if not _initialized:
        _initialize_firebase()
    return _db


def get_auth():
    """Get Firebase Auth client."""
    if not _initialized:
        _initialize_firebase()
    return _auth_client


def get_bucket():
    """Get Firebase Storage bucket."""
    if not _initialized:
        _initialize_firebase()
    return _bucket
