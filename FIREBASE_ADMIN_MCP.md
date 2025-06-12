# Firebase Admin MCP

A Django app that implements a complete Firebase Model Context Protocol (MCP) server, exposing Firebase Authentication, Firestore Database, and Cloud Storage services as MCP tools.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)
- [LangChain Integration](#langchain-integration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

The Firebase Admin MCP app bridges Firebase services with the Model Context Protocol, allowing AI agents and other MCP clients to interact with Firebase backend services through a standardized protocol. It provides both HTTP and stdio transport options and integrates seamlessly with Django applications.

### Key Benefits

- **🔥 Real Firebase Integration**: Direct access to Firebase services (not mocked)
- **🌐 MCP Protocol Compliance**: Implements JSON-RPC 2.0 over HTTP and stdio
- **🤖 AI Agent Ready**: Perfect for LangChain agents and other AI systems
- **🔧 Django Native**: Seamless integration with existing Django projects
- **⚡ Async Support**: Proper async handling for all Firebase operations
- **🛡️ Error Handling**: Comprehensive error handling and validation

## ✨ Features

### Firebase Services Supported

#### 🔐 Firebase Authentication (4 tools)

- **verify_id_token**: Verify Firebase ID tokens
- **create_custom_token**: Create custom authentication tokens
- **get_user**: Retrieve user information by UID
- **delete_user**: Delete user accounts

#### 📚 Firestore Database (6 tools)

- **get_document**: Retrieve documents from collections
- **create_document**: Create new documents
- **update_document**: Update existing documents
- **delete_document**: Delete documents
- **list_collections**: List all collections
- **query_collection**: Query documents with filters

#### 🗄️ Cloud Storage (4 tools)

- **upload_file**: Upload files to Firebase Storage
- **download_file**: Download files from Firebase Storage
- **list_files**: List files with optional prefix filtering
- **delete_file**: Delete files from storage

### Transport Options

- **HTTP Server**: JSON-RPC 2.0 over HTTP (`/mcp/` endpoint)
- **Stdio**: Standard input/output for MCP clients
- **Management Command**: `python manage.py run_mcp`

## 🏗️ Architecture

```
firebase_admin_mcp/
├── __init__.py                 # App package initialization
├── apps.py                     # Django app configuration
├── firebase_init.py            # Firebase SDK initialization
├── views.py                    # HTTP endpoint handlers
├── urls.py                     # URL routing
├── models.py                   # Django models (if needed)
├── admin.py                    # Django admin configuration
├── tools/                      # Firebase MCP tools
│   ├── __init__.py
│   ├── auth.py                 # Authentication tools
│   ├── firestore.py           # Firestore database tools
│   └── storage.py             # Cloud Storage tools
├── management/                 # Django management commands
│   └── commands/
│       └── run_mcp.py         # MCP server command
└── tests/                     # Test suite
    ├── __init__.py
    └── test_tools.py          # Tool tests
```

### Component Overview

1. **Firebase Initialization** (`firebase_init.py`): Lazy-loaded Firebase Admin SDK setup
2. **MCP Tools** (`tools/`): Individual Firebase service implementations
3. **HTTP Handler** (`views.py`): JSON-RPC 2.0 HTTP endpoint
4. **Management Command** (`management/commands/`): CLI server runner
5. **URL Configuration** (`urls.py`): Django URL routing

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Django 4.0+
- Firebase project with Admin SDK credentials
- Firebase services enabled (Auth, Firestore, Storage)

### 1. Install Dependencies

```bash
pip install django>=4.0
pip install firebase-admin>=6.0.0
pip install mcp[cli]>=0.1.0
pip install djangorestframework>=3.14
pip install python-dotenv>=1.0.0
```

### 2. Add to Django Project

Add to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'rest_framework',
    'firebase_admin_mcp',
]
```

### 3. Include URLs

Add to your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your other URLs
    path('mcp/', include('firebase_admin_mcp.urls')),
]
```

## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file in your project root:

```env
# Firebase Configuration
SERVICE_ACCOUNT_KEY_PATH=path/to/your/firebase-credentials.json
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com

# MCP Configuration
MCP_TRANSPORT=http  # or 'stdio'
MCP_HOST=127.0.0.1
MCP_PORT=8001
```

### 2. Django Settings

Add to your `settings.py`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firebase MCP Configuration
FIREBASE_MCP = {
    'SERVICE_ACCOUNT_KEY_PATH': os.getenv('SERVICE_ACCOUNT_KEY_PATH'),
    'STORAGE_BUCKET': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'MCP_TRANSPORT': os.getenv('MCP_TRANSPORT', 'http'),
    'MCP_HOST': os.getenv('MCP_HOST', '127.0.0.1'),
    'MCP_PORT': int(os.getenv('MCP_PORT', '8001')),
}
```

### 3. Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings → Service Accounts
4. Click "Generate new private key"
5. Save the JSON file securely
6. Update `SERVICE_ACCOUNT_KEY_PATH` in `.env`

## 🔧 Usage

### Starting the MCP Server

#### Option 1: Django Development Server (HTTP)

```bash
python manage.py runserver 8001
```

The MCP endpoint will be available at: `http://127.0.0.1:8001/mcp/`

#### Option 2: Dedicated MCP Command (HTTP or Stdio)

```bash
# HTTP transport
python manage.py run_mcp --transport http --host 127.0.0.1 --port 8001

# Stdio transport (for MCP clients)
python manage.py run_mcp --transport stdio
```

### Testing the Server

#### Quick Health Check

```bash
curl http://127.0.0.1:8001/mcp/
```

Should return server information and available tools.

#### List Available Tools

```bash
curl -X POST http://127.0.0.1:8001/mcp/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

#### Call a Tool

```bash
curl -X POST http://127.0.0.1:8001/mcp/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "list_collections",
      "arguments": {}
    },
    "id": 2
  }'
```

## 📚 API Reference

### HTTP Endpoints

#### GET /mcp/

Returns server information and available tools.

**Response:**

```json
{
  "name": "Firebase MCP Server",
  "version": "1.0.0",
  "description": "Firebase Admin SDK MCP Server for Django",
  "tools": [...]
}
```

#### POST /mcp/

Handles JSON-RPC 2.0 method calls.

**Request Format:**

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {...}
  },
  "id": 1
}
```

### Available Tools

#### Authentication Tools

##### verify_id_token

Verify a Firebase ID token.

**Parameters:**

- `id_token` (string): Firebase ID token to verify

**Example:**

```json
{
  "name": "verify_id_token",
  "arguments": {
    "id_token": "eyJhbGciOiJSUzI1NiIs..."
  }
}
```

##### create_custom_token

Create a custom Firebase token.

**Parameters:**

- `uid` (string): User ID
- `additional_claims` (object, optional): Additional token claims

##### get_user

Get user information by UID.

**Parameters:**

- `uid` (string): User ID to look up

##### delete_user

Delete a user account.

**Parameters:**

- `uid` (string): User ID to delete

#### Firestore Tools

##### get_document

Retrieve a document from Firestore.

**Parameters:**

- `collection` (string): Collection name
- `document_id` (string): Document ID

**Example:**

```json
{
  "name": "get_document",
  "arguments": {
    "collection": "users",
    "document_id": "user123"
  }
}
```

##### create_document

Create a new document in Firestore.

**Parameters:**

- `collection` (string): Collection name
- `data` (object): Document data
- `document_id` (string, optional): Document ID (auto-generated if not provided)

##### update_document

Update an existing document.

**Parameters:**

- `collection` (string): Collection name
- `document_id` (string): Document ID
- `data` (object): Data to update

##### delete_document

Delete a document from Firestore.

**Parameters:**

- `collection` (string): Collection name
- `document_id` (string): Document ID

##### list_collections

List all collections in Firestore.

**Parameters:** None

##### query_collection

Query documents from a collection.

**Parameters:**

- `collection` (string): Collection name
- `limit` (integer, optional): Maximum number of results

#### Storage Tools

##### upload_file

Upload a file to Firebase Storage.

**Parameters:**

- `file_path` (string): Remote path in storage
- `local_path` (string): Local file path
- `content_type` (string, optional): File content type

##### download_file

Download a file from Firebase Storage.

**Parameters:**

- `file_path` (string): Remote path in storage
- `local_path` (string): Local path to save file

##### list_files

List files in Firebase Storage.

**Parameters:**

- `prefix` (string, optional): Path prefix filter
- `max_results` (integer, optional): Maximum results

##### delete_file

Delete a file from Firebase Storage.

**Parameters:**

- `file_path` (string): Remote path to delete

## 🧪 Testing

### Run Test Suite

```bash
# Run comprehensive MCP tests
python test_mcp_complete.py

# Run Firebase connectivity tests
python test_firebase_connection.py

# Run Django tests (if implemented)
python manage.py test firebase_admin_mcp
```

### Manual Testing

```python
import requests
import json

# Test server connection
response = requests.get('http://127.0.0.1:8001/mcp/')
print(response.json())

# Test Firestore
payload = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "list_collections",
        "arguments": {}
    },
    "id": 1
}
response = requests.post('http://127.0.0.1:8001/mcp/', json=payload)
print(response.json())
```

## 🤖 LangChain Integration

The app includes a LangChain client for seamless AI agent integration.

### Installation

```python
from tools.agents.firebase_mcp_client import (
    firestore_list_collections,
    firestore_create_document,
    storage_list_files,
    ALL_FIREBASE_TOOLS
)
```

### Usage with LangChain Agents

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.agents.firebase_mcp_client import ALL_FIREBASE_TOOLS

# Create agent with Firebase tools
model = ChatOpenAI(model="gpt-4")
agent = create_react_agent(
    model=model,
    tools=ALL_FIREBASE_TOOLS,
    prompt="You are a helpful assistant with access to Firebase services."
)

# Use the agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "List all Firestore collections"}]
})
```

### Enhanced Dummy Agent

Your existing agents can automatically use Firebase tools:

```python
from tools.agents.dummy_agent import create_dummy_agent

# Automatically detects and uses Firebase MCP tools
agent = create_dummy_agent()
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Server Not Starting

**Problem:** `python manage.py runserver` fails

**Solutions:**

- Check Django configuration: `python manage.py check`
- Verify dependencies are installed
- Check `.env` file exists and has correct paths

#### 2. Firebase Connection Errors

**Problem:** "Default app does not exist" or credential errors

**Solutions:**

- Verify `SERVICE_ACCOUNT_KEY_PATH` points to valid JSON file
- Check Firebase project permissions
- Ensure Firebase services are enabled in console

#### 3. MCP Tools Not Found

**Problem:** "Tool not found" errors

**Solutions:**

- Restart Django server after changes
- Check tool imports in `views.py`
- Verify MCP server is running

#### 4. CORS Issues

**Problem:** Browser requests failing

**Solutions:**

- CORS headers are included in responses
- Use server-to-server requests for production
- Check firewall/network settings

### Debug Mode

Enable debug logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'firebase_admin_mcp': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Performance Considerations

- **Connection Pooling**: Firebase Admin SDK handles connection pooling automatically
- **Rate Limits**: Be aware of Firebase quota limits
- **Async Operations**: All tools use proper async handling
- **Memory Usage**: Firebase SDK maintains connection state

## 🔒 Security Considerations

### Best Practices

1. **Secure Credentials**: Store Firebase credentials securely
2. **Environment Variables**: Use `.env` files, never commit credentials
3. **Network Security**: Use HTTPS in production
4. **Access Control**: Implement proper Firebase security rules
5. **Input Validation**: All inputs are validated before Firebase calls

### Production Deployment

```python
# settings.py - Production
FIREBASE_MCP = {
    'SERVICE_ACCOUNT_KEY_PATH': '/secure/path/to/credentials.json',
    'STORAGE_BUCKET': 'your-production-bucket.appspot.com',
    'MCP_TRANSPORT': 'http',
    'MCP_HOST': '0.0.0.0',  # For external access
    'MCP_PORT': int(os.getenv('PORT', '8000')),
}

# Use environment variables for all sensitive data
```

## 📖 Advanced Usage

### Custom Tool Development

Add new Firebase tools by extending the existing pattern:

```python
# firebase_admin_mcp/tools/custom.py
import asyncio
from firebase_admin_mcp.firebase_init import get_db

async def custom_firebase_operation(param1: str, param2: int):
    """Custom Firebase operation."""
    db = get_db()

    # Your custom logic here
    result = await asyncio.to_thread(
        # Your Firebase operation
    )

    return {"status": "success", "data": result}
```

Register in `views.py`:

```python
from .tools import custom

TOOLS['custom_operation'] = custom.custom_firebase_operation
```

### Integration with Other MCP Clients

The server works with any MCP-compatible client:

```bash
# Claude Desktop MCP config
{
  "mcpServers": {
    "firebase": {
      "command": "python",
      "args": ["manage.py", "run_mcp", "--transport", "stdio"],
      "cwd": "/path/to/your/django/project"
    }
  }
}
```

## 🤝 Contributing

### Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Firebase project and credentials
4. Run tests: `python test_mcp_complete.py`

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Include error handling
- Write tests for new features

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request with description

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙋 Support

### Documentation

- [Firebase Admin SDK Documentation](https://firebase.google.com/docs/admin/setup)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Django Documentation](https://docs.djangoproject.com/)

### Getting Help

1. Check the troubleshooting section above
2. Review Firebase console for service status
3. Check Django logs for error details
4. Verify MCP server is accessible

### Version History

- **v1.0.0**: Initial release with full Firebase MCP implementation
  - 14 Firebase tools (Auth, Firestore, Storage)
  - HTTP and stdio transport support
  - LangChain integration
  - Comprehensive test suite

---

**Made with ❤️ for the AI agent community**

_This Django app brings the power of Firebase to AI agents through the Model Context Protocol, enabling seamless backend integration for intelligent applications._
