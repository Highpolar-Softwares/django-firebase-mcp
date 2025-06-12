"""
Firestore database tools for MCP server.
"""
import asyncio
from typing import Dict, List, Optional, Any
from google.cloud.firestore import Query
from ..firebase_init import get_db


async def get_document(collection: str, doc_id: str) -> dict:
    """
    Get a document from Firestore.

    Args:
        collection: The collection name
        doc_id: The document ID

    Returns:
        dict: Document data or empty dict if not found
    """
    def _get():
        db = get_db()
        doc_ref = db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data['_id'] = doc.id
            return data
        return {}

    return await asyncio.to_thread(_get)


async def create_document(collection: str, data: dict) -> str:
    """
    Create a new document in Firestore.

    Args:
        collection: The collection name
        data: The document data

    Returns:
        str: The created document ID
    """
    def _create():
        db = get_db()
        doc_ref = db.collection(collection).document()
        doc_ref.set(data)
        return doc_ref.id

    return await asyncio.to_thread(_create)


async def update_document(collection: str, doc_id: str, data: dict) -> bool:
    """
    Update an existing document in Firestore.

    Args:
        collection: The collection name
        doc_id: The document ID
        data: The updated data

    Returns:
        bool: True if successful
    """
    def _update():
        db = get_db()
        doc_ref = db.collection(collection).document(doc_id)
        doc_ref.update(data)
        return True

    return await asyncio.to_thread(_update)


async def delete_document(collection: str, doc_id: str) -> bool:
    """
    Delete a document from Firestore.

    Args:
        collection: The collection name
        doc_id: The document ID

    Returns:
        bool: True if successful
    """
    def _delete():
        db = get_db()
        doc_ref = db.collection(collection).document(doc_id)
        doc_ref.delete()
        return True

    return await asyncio.to_thread(_delete)


async def list_collections() -> List[str]:
    """
    List all collections in Firestore.

    Returns:
        List[str]: List of collection names
    """
    def _list():
        db = get_db()
        collections = db.collections()
        return [col.id for col in collections]

    return await asyncio.to_thread(_list)


async def query_collection(
    collection: str,
    filters: Optional[dict] = None,
    order_by: Optional[List[str]] = None,
    limit: Optional[int] = None
) -> List[dict]:
    """
    Query documents from a Firestore collection.

    Args:
        collection: The collection name
        filters: Dict of field filters (e.g., {"field": "value", "age": {">=": 18}})
        order_by: List of fields to order by
        limit: Maximum number of documents to return

    Returns:
        List[dict]: List of matching documents
    """
    def _query():
        db = get_db()
        query = db.collection(collection)

        # Apply filters
        if filters:
            for field, value in filters.items():
                if isinstance(value, dict):
                    # Handle operators like {">=": 18}
                    for op, val in value.items():
                        query = query.where(field, op, val)
                else:
                    # Simple equality filter
                    query = query.where(field, "==", value)

        # Apply ordering
        if order_by:
            for field in order_by:
                if field.startswith('-'):
                    query = query.order_by(
                        field[1:], direction=Query.DESCENDING)
                else:
                    query = query.order_by(field)

        # Apply limit
        if limit:
            query = query.limit(limit)

        docs = query.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['_id'] = doc.id
            results.append(data)

        return results

    return await asyncio.to_thread(_query)
