#!/usr/bin/env python3
from firebase_admin_mcp.firebase_init import get_db, get_auth, get_bucket
import os
import django

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_firebase_mcp.settings'
django.setup()


def test_firebase_connection():
    print('Testing Firebase connection...')

    # Test Firestore
    try:
        db = get_db()
        print(f'✓ Firestore client: {type(db)}')

        # Try to get a reference (this doesn't make a network call)
        test_ref = db.collection('test').document('test')
        print(f'✓ Firestore reference created: {test_ref.id}')

    except Exception as e:
        print(f'✗ Firestore error: {e}')

    # Test Auth
    try:
        auth = get_auth()
        print(f'✓ Auth client: {type(auth)}')
    except Exception as e:
        print(f'✗ Auth error: {e}')

    # Test Storage
    try:
        bucket = get_bucket()
        print(f'✓ Storage bucket: {bucket.name if bucket else "None"}')
    except Exception as e:
        print(f'✗ Storage error: {e}')


if __name__ == '__main__':
    test_firebase_connection()
