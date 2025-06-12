"""
Tests for Firebase MCP tools.
"""
import asyncio
from unittest.mock import Mock, patch


async def test_get_document():
    """Test get_document tool with mocked Firestore."""
    # Import here to avoid Django settings issues
    from ..tools.firestore import get_document

    # Mock the Firestore client and document
    mock_doc = Mock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {'name': 'Test User', 'age': 30}
    mock_doc.id = 'test_doc_id'

    mock_doc_ref = Mock()
    mock_doc_ref.get.return_value = mock_doc

    mock_collection = Mock()
    mock_collection.document.return_value = mock_doc_ref

    # Patch the get_db function
    with patch('firebase_admin_mcp.firebase_init.get_db') as mock_get_db:
        mock_db = Mock()
        mock_db.collection.return_value = mock_collection
        mock_get_db.return_value = mock_db

        # Test the tool
        result = await get_document('users', 'test_doc_id')

        # Verify the result
        expected = {
            'name': 'Test User',
            'age': 30,
            '_id': 'test_doc_id'
        }
        assert result == expected
        print("✓ get_document test passed")


async def test_get_document_not_found():
    """Test get_document tool when document doesn't exist."""
    from ..tools.firestore import get_document

    # Mock non-existent document
    mock_doc = Mock()
    mock_doc.exists = False

    mock_doc_ref = Mock()
    mock_doc_ref.get.return_value = mock_doc

    mock_collection = Mock()
    mock_collection.document.return_value = mock_doc_ref

    with patch('firebase_admin_mcp.firebase_init.get_db') as mock_get_db:
        mock_db = Mock()
        mock_db.collection.return_value = mock_collection
        mock_get_db.return_value = mock_db

        # Test the tool
        result = await get_document('users', 'nonexistent_id')

        # Should return empty dict
        assert result == {}
        print("✓ get_document_not_found test passed")


def run_tests():
    """Run all tests."""
    try:
        asyncio.run(test_get_document())
        asyncio.run(test_get_document_not_found())
        print("All tests passed!")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("Running Firebase MCP tools tests...")
    run_tests()
