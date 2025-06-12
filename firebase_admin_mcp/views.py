"""
HTTP endpoint for Firebase MCP server.
"""
from .tools import auth, firestore, storage
import json
import asyncio
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from asgiref.sync import async_to_sync

# Custom JSON encoder for Firebase objects


class FirebaseJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Firebase-specific objects."""

    def default(self, obj):
        # Handle Firebase DatetimeWithNanoseconds
        if hasattr(obj, 'timestamp'):
            # Convert to ISO format string
            return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)
        # Handle standard datetime objects
        elif isinstance(obj, datetime):
            return obj.isoformat()
        # Handle other non-serializable objects
        elif hasattr(obj, '__dict__'):
            return str(obj)
        return super().default(obj)


def safe_json_dumps(obj, **kwargs):
    """Safely serialize objects to JSON, handling Firebase objects."""
    return json.dumps(obj, cls=FirebaseJSONEncoder, **kwargs)


# Import all tool modules to register the tools

# Store all available tools
TOOLS = {
    'verify_id_token': auth.verify_id_token,
    'create_custom_token': auth.create_custom_token,
    'get_user': auth.get_user,
    'delete_user': auth.delete_user,
    'get_document': firestore.get_document,
    'create_document': firestore.create_document,
    'update_document': firestore.update_document,
    'delete_document': firestore.delete_document,
    'list_collections': firestore.list_collections,
    'query_collection': firestore.query_collection,
    'upload_file': storage.upload_file,
    'download_file': storage.download_file,
    'delete_file': storage.delete_file,
    'list_files': storage.list_files,
}

# Tool descriptions for MCP protocol
TOOL_DESCRIPTIONS = {
    'verify_id_token': {
        'name': 'verify_id_token',
        'description': 'Verify Firebase ID token',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'id_token': {'type': 'string', 'description': 'Firebase ID token to verify'}
            },
            'required': ['id_token']
        }
    },
    'create_custom_token': {
        'name': 'create_custom_token',
        'description': 'Create Firebase custom token',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'uid': {'type': 'string', 'description': 'User ID'},
                'additional_claims': {'type': 'object', 'description': 'Additional claims (optional)'}
            },
            'required': ['uid']
        }
    },
    'get_user': {
        'name': 'get_user',
        'description': 'Get Firebase user information',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'uid': {'type': 'string', 'description': 'User ID'}
            },
            'required': ['uid']
        }
    },
    'delete_user': {
        'name': 'delete_user',
        'description': 'Delete Firebase user',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'uid': {'type': 'string', 'description': 'User ID to delete'}
            },
            'required': ['uid']
        }
    },
    'get_document': {
        'name': 'get_document',
        'description': 'Get Firestore document',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'collection': {'type': 'string', 'description': 'Collection name'},
                'document_id': {'type': 'string', 'description': 'Document ID'}
            },
            'required': ['collection', 'document_id']
        }
    },
    'create_document': {
        'name': 'create_document',
        'description': 'Create Firestore document',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'collection': {'type': 'string', 'description': 'Collection name'},
                'document_id': {'type': 'string', 'description': 'Document ID (optional)'},
                'data': {'type': 'object', 'description': 'Document data'}
            },
            'required': ['collection', 'data']
        }
    },
    'update_document': {
        'name': 'update_document',
        'description': 'Update Firestore document',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'collection': {'type': 'string', 'description': 'Collection name'},
                'document_id': {'type': 'string', 'description': 'Document ID'},
                'data': {'type': 'object', 'description': 'Document data to update'}
            },
            'required': ['collection', 'document_id', 'data']
        }
    },
    'delete_document': {
        'name': 'delete_document',
        'description': 'Delete Firestore document',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'collection': {'type': 'string', 'description': 'Collection name'},
                'document_id': {'type': 'string', 'description': 'Document ID'}
            },
            'required': ['collection', 'document_id']
        }
    },
    'list_collections': {
        'name': 'list_collections',
        'description': 'List Firestore collections',
        'inputSchema': {
            'type': 'object',
            'properties': {},
            'required': []
        }
    },
    'query_collection': {
        'name': 'query_collection',
        'description': 'Query Firestore collection',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'collection': {'type': 'string', 'description': 'Collection name'},
                'limit': {'type': 'integer', 'description': 'Limit results (optional)'}
            },
            'required': ['collection']
        }
    },
    'upload_file': {
        'name': 'upload_file',
        'description': 'Upload file to Firebase Storage',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'file_path': {'type': 'string', 'description': 'Remote file path in storage'},
                'local_path': {'type': 'string', 'description': 'Local file path to upload'},
                'content_type': {'type': 'string', 'description': 'Content type (optional)'}
            },
            'required': ['file_path', 'local_path']
        }
    },
    'download_file': {
        'name': 'download_file',
        'description': 'Download file from Firebase Storage',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'file_path': {'type': 'string', 'description': 'Remote file path in storage'},
                'local_path': {'type': 'string', 'description': 'Local path to save file'}
            },
            'required': ['file_path', 'local_path']
        }
    },
    'delete_file': {
        'name': 'delete_file',
        'description': 'Delete file from Firebase Storage',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'file_path': {'type': 'string', 'description': 'Remote file path in storage'}
            },
            'required': ['file_path']
        }
    },
    'list_files': {
        'name': 'list_files',
        'description': 'List files in Firebase Storage',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'prefix': {'type': 'string', 'description': 'Path prefix (optional)'},
                'max_results': {'type': 'integer', 'description': 'Maximum results (optional)'}
            },
            'required': []
        }
    }
}


@api_view(['POST', 'GET', 'OPTIONS'])
def mcp_handler(request):
    """
    Handle MCP HTTP requests directly without using FastMCP's Starlette app.

    This implements the basic MCP HTTP protocol:
    - GET requests return server info and available tools
    - POST requests handle JSON-RPC 2.0 method calls
    """
    try:
        # Handle CORS preflight
        if request.method == 'OPTIONS':
            response = HttpResponse('')
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        # Handle GET requests - return server info
        if request.method == 'GET':
            server_info = {
                'name': 'Firebase MCP Server',
                'version': '1.0.0',
                'description': 'Firebase Admin SDK MCP Server for Django',
                'tools': list(TOOL_DESCRIPTIONS.values())
            }
            response = HttpResponse(
                json.dumps(server_info, indent=2),
                content_type='application/json'
            )
            response['Access-Control-Allow-Origin'] = '*'
            return response

        # Handle POST requests - JSON-RPC 2.0 calls
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return HttpResponse(
                    json.dumps({
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32700,
                            'message': 'Parse error'
                        },
                        'id': None
                    }),
                    content_type='application/json',
                    status=400
                )

            # Validate JSON-RPC 2.0 format
            if not isinstance(data, dict) or data.get('jsonrpc') != '2.0':
                return HttpResponse(
                    json.dumps({
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32600,
                            'message': 'Invalid Request'
                        },
                        'id': data.get('id')
                    }),
                    content_type='application/json',
                    status=400
                )

            method = data.get('method')
            params = data.get('params', {})
            request_id = data.get('id')

            # Handle tools/list method
            if method == 'tools/list':
                response_data = {
                    'jsonrpc': '2.0',
                    'result': {
                        'tools': list(TOOL_DESCRIPTIONS.values())
                    },
                    'id': request_id
                }
                response = HttpResponse(
                    json.dumps(response_data),
                    content_type='application/json'
                )
                response['Access-Control-Allow-Origin'] = '*'
                return response

            # Handle tools/call method
            elif method == 'tools/call':
                tool_name = params.get('name')
                tool_arguments = params.get('arguments', {})

                if tool_name not in TOOLS:
                    response_data = {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32601,
                            'message': f'Tool not found: {tool_name}'
                        },
                        'id': request_id
                    }
                    response = HttpResponse(
                        json.dumps(response_data),
                        content_type='application/json',
                        status=404
                    )
                    response['Access-Control-Allow-Origin'] = '*'
                    return response

                try:                    # Call the tool function
                    tool_func = TOOLS[tool_name]
                    result = async_to_sync(tool_func)(**tool_arguments)

                    response_data = {
                        'jsonrpc': '2.0',
                        'result': {
                            'content': [
                                {
                                    'type': 'text',
                                    'text': safe_json_dumps(result, indent=2)
                                }
                            ]
                        },
                        'id': request_id
                    }
                    response = HttpResponse(
                        json.dumps(response_data),
                        content_type='application/json'
                    )
                    response['Access-Control-Allow-Origin'] = '*'
                    return response

                except Exception as e:
                    response_data = {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32000,
                            'message': f'Tool execution error: {str(e)}'
                        },
                        'id': request_id
                    }
                    response = HttpResponse(
                        safe_json_dumps(response_data),
                        content_type='application/json',
                        status=500
                    )
                    response['Access-Control-Allow-Origin'] = '*'
                    return response

            # Unknown method
            else:
                response_data = {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32601,
                        'message': f'Method not found: {method}'
                    },
                    'id': request_id
                }
                response = HttpResponse(
                    json.dumps(response_data),
                    content_type='application/json',
                    status=404
                )
                response['Access-Control-Allow-Origin'] = '*'
                return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        response_data = {
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'message': f'Internal server error: {str(e)}'
            },
            'id': None
        }
        response = HttpResponse(
            json.dumps(response_data),
            content_type='application/json',
            status=500
        )
        response['Access-Control-Allow-Origin'] = '*'
        return response
