#!/usr/bin/env python3
from firebase_admin_mcp.tools.firestore import create_document, get_document, list_collections
import os
import django
import asyncio

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_firebase_mcp.settings'
django.setup()


async def test_firestore_operations():
    print('Testing Firestore operations...')
    try:
        # Test 1: List collections
        print('1. Testing list_collections...')
        collections = await list_collections()
        print(f'   Collections found: {len(collections)} - {collections[:3]}...' if len(
            collections) > 3 else f'   Collections: {collections}')

        # Test 2: Create a document
        print('2. Testing create_document...')
        test_data = {
            'name': 'MCP Test User',
            'email': 'mcptest@example.com',
            'age': 25,
            'timestamp': '2025-06-11T10:00:00Z'
        }
        doc_id = await create_document('mcp_test', test_data)
        print(f'   ✓ Created document with ID: {doc_id}')

        # Test 3: Get the document
        print('3. Testing get_document...')
        retrieved_doc = await get_document('mcp_test', doc_id)
        print(
            f'   ✓ Retrieved document: {retrieved_doc["name"]} ({retrieved_doc["email"]})')

        return True

    except Exception as e:
        print(f'   ✗ Error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    result = asyncio.run(test_firestore_operations())
    print(f'\nFirestore test {"PASSED" if result else "FAILED"}')
