#!/usr/bin/env python3
from firebase_admin_mcp.tools.firestore import create_document, get_document, list_collections
import os
import django
import asyncio

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_firebase_mcp.settings'
django.setup()


async def test_firestore():
    print('Testing Firestore operations...')
    try:
        # Test list collections first
        collections = await list_collections()
        print(f'✓ Existing collections: {collections}')

        # Create a test document
        test_data = {'name': 'Test User',
                     'email': 'test@example.com', 'age': 25}
        doc_id = await create_document('test_collection', test_data)
        print(f'✓ Created document with ID: {doc_id}')

        # Get the document back
        retrieved_doc = await get_document('test_collection', doc_id)
        print(f'✓ Retrieved document: {retrieved_doc}')

        return True
    except Exception as e:
        print(f'✗ Error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_firestore())
