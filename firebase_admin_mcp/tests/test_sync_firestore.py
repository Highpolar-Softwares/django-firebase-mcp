#!/usr/bin/env python3
from firebase_admin_mcp.firebase_init import get_db
import os
import django

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_firebase_mcp.settings'
django.setup()


def test_firestore_sync():
    print('Testing synchronous Firestore operations...')
    try:
        db = get_db()
        print(f'✓ Got Firestore client: {type(db)}')

        # Create a simple document synchronously
        doc_ref = db.collection('test_sync').document()
        doc_ref.set({
            'message': 'Hello from MCP test',
            'timestamp': '2025-06-11'
        })
        print(f'✓ Created document with ID: {doc_ref.id}')

        # Read it back
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            print(f'✓ Retrieved document: {data}')
        else:
            print('✗ Document not found')

        return True

    except Exception as e:
        print(f'✗ Error: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    test_firestore_sync()
