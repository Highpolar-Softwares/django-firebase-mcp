"""
Firebase Cloud Storage tools for MCP server.
"""
import asyncio
import base64
from typing import List
from ..firebase_init import get_bucket


async def upload_file(path: str, b64_data: str) -> str:
    """
    Upload a file to Firebase Cloud Storage.

    Args:
        path: The storage path for the file
        b64_data: Base64 encoded file data

    Returns:
        str: Public URL of the uploaded file
    """
    def _upload():
        bucket = get_bucket()
        # Decode base64 data
        file_data = base64.b64decode(b64_data)

        # Upload to storage
        blob = bucket.blob(path)
        blob.upload_from_string(file_data)

        # Make publicly accessible
        blob.make_public()

        return blob.public_url

    return await asyncio.to_thread(_upload)


async def download_file(path: str) -> str:
    """
    Download a file from Firebase Cloud Storage.

    Args:
        path: The storage path of the file

    Returns:
        str: Base64 encoded file data
    """
    def _download():
        bucket = get_bucket()
        blob = bucket.blob(path)
        file_data = blob.download_as_bytes()
        return base64.b64encode(file_data).decode('utf-8')

    return await asyncio.to_thread(_download)


async def delete_file(path: str) -> bool:
    """
    Delete a file from Firebase Cloud Storage.

    Args:
        path: The storage path of the file to delete

    Returns:
        bool: True if successful
    """
    def _delete():
        bucket = get_bucket()
        blob = bucket.blob(path)
        blob.delete()
        return True

    return await asyncio.to_thread(_delete)


async def list_files(prefix: str = "") -> List[str]:
    """
    List files in Firebase Cloud Storage.

    Args:
        prefix: Optional prefix to filter files

    Returns:
        List[str]: List of file paths
    """
    def _list():
        bucket = get_bucket()
        blobs = bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    return await asyncio.to_thread(_list)
