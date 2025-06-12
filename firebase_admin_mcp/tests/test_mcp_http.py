#!/usr/bin/env python3
"""
Test the Firebase MCP HTTP endpoint
"""
import requests
import json

# Test server info
print("=== Testing MCP HTTP Endpoint ===")
print("1. Testing GET request (server info)...")

try:
    response = requests.get('http://127.0.0.1:8001/mcp/')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n2. Testing tools/list method...")

# Test tools/list
try:
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }
    response = requests.post(
        'http://127.0.0.1:8001/mcp/',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n3. Testing tools/call method (list_collections)...")

# Test tools/call
try:
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "list_collections",
            "arguments": {}
        },
        "id": 2
    }
    response = requests.post(
        'http://127.0.0.1:8001/mcp/',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n4. Testing tools/call method (get_document)...")

# Test get_document
try:
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_document",
            "arguments": {
                "collection": "test_collection",
                "document_id": "test_doc"
            }
        },
        "id": 3
    }
    response = requests.post(
        'http://127.0.0.1:8001/mcp/',
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Test Complete ===")
