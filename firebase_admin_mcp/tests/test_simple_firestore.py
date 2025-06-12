#!/usr/bin/env python3
import time
from firebase_admin_mcp.firebase_init import get_db
import os
import django
import sys

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_firebase_mcp.settings'
django.setup()


def test_firestore_simple():
    print('Testing simple Firestore operation...')
    try:
        db = get_db()
        print(f'✓ Got Firestore client')

        # Test collection reference (no network call)
        test_collection = db.collection('mcp_test')
        print(f'✓ Got collection reference: {test_collection.id}')

        # Test creating a document reference (no network call)
        doc_ref = test_collection.document('test_doc_1')
        print(f'✓ Got document reference: {doc_ref.id}')

        # Try a quick set operation with timeout
        print('   Attempting to set document data...')
        start_time = time.time()

        doc_ref.set({
            'message': 'Hello from Firebase MCP test',
            'timestamp': time.time(),
            'test_type': 'basic_connectivity'
        })

        elapsed = time.time() - start_time
        print(f'✓ Document set successfully in {elapsed:.2f} seconds')

        # Try to read it back
        print('   Attempting to read document...')
        start_time = time.time()

        doc_snapshot = doc_ref.get()
        elapsed = time.time() - start_time

        if doc_snapshot.exists:
            data = doc_snapshot.to_dict()
            print(f'✓ Document read successfully in {elapsed:.2f} seconds')
            print(f'   Data: {data["message"]}')
        else:
            print('✗ Document not found')

        return True

    except Exception as e:
        print(f'✗ Error: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    result = test_firestore_simple()
    print(f'\nFirestore connectivity test {"PASSED" if result else "FAILED"}')
