#!/usr/bin/env python3
from firebase_admin_mcp.tools.firestore import create_document, get_document, update_document, delete_document, list_collections
import os
import django
import asyncio
import time

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_firebase_mcp.settings'
django.setup()


async def test_firestore_mcp_tools():
    print('Testing Firebase MCP Firestore tools...')

    try:
        # Test 1: List collections
        print('\n1. Testing list_collections...')
        start_time = time.time()
        collections = await list_collections()
        elapsed = time.time() - start_time
        print(f'   ✓ Found {len(collections)} collections in {elapsed:.2f}s')
        if collections:
            print(
                f'   Collections: {collections[:5]}{"..." if len(collections) > 5 else ""}')

        # Test 2: Create document
        print('\n2. Testing create_document...')
        test_data = {
            'name': 'MCP Test User',
            'email': 'mcptest@example.com',
            'age': 30,
            'skills': ['Python', 'Firebase', 'MCP'],
            'created_at': time.time()
        }
        start_time = time.time()
        doc_id = await create_document('mcp_test_collection', test_data)
        elapsed = time.time() - start_time
        print(f'   ✓ Created document with ID: {doc_id} in {elapsed:.2f}s')

        # Test 3: Get document
        print('\n3. Testing get_document...')
        start_time = time.time()
        retrieved_doc = await get_document('mcp_test_collection', doc_id)
        elapsed = time.time() - start_time
        print(f'   ✓ Retrieved document in {elapsed:.2f}s')
        print(f'   Data: {retrieved_doc["name"]} ({retrieved_doc["email"]})')
        print(f'   Skills: {retrieved_doc["skills"]}')

        # Test 4: Update document
        print('\n4. Testing update_document...')
        update_data = {
            'age': 31,
            'skills': ['Python', 'Firebase', 'MCP', 'Django'],
            'updated_at': time.time()
        }
        start_time = time.time()
        update_result = await update_document('mcp_test_collection', doc_id, update_data)
        elapsed = time.time() - start_time
        print(f'   ✓ Updated document in {elapsed:.2f}s: {update_result}')

        # Test 5: Get updated document
        print('\n5. Testing get updated document...')
        start_time = time.time()
        updated_doc = await get_document('mcp_test_collection', doc_id)
        elapsed = time.time() - start_time
        print(f'   ✓ Retrieved updated document in {elapsed:.2f}s')
        print(
            f'   Updated age: {updated_doc["age"]}, Skills: {updated_doc["skills"]}')

        # Test 6: Delete document
        print('\n6. Testing delete_document...')
        start_time = time.time()
        delete_result = await delete_document('mcp_test_collection', doc_id)
        elapsed = time.time() - start_time
        print(f'   ✓ Deleted document in {elapsed:.2f}s: {delete_result}')

        # Test 7: Verify deletion
        print('\n7. Testing document deletion verification...')
        start_time = time.time()
        deleted_doc = await get_document('mcp_test_collection', doc_id)
        elapsed = time.time() - start_time
        print(f'   ✓ Verified deletion in {elapsed:.2f}s')
        print(f'   Document exists: {bool(deleted_doc)}')

        return True

    except Exception as e:
        print(f'   ✗ Error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print('Firebase MCP Tools Comprehensive Test')
    print('=' * 50)
    result = asyncio.run(test_firestore_mcp_tools())
    print(f'\n{"="*50}')
    print(f'Firestore MCP tools test {"PASSED" if result else "FAILED"}')
