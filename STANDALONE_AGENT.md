# Standalone Firebase Agent

A completely self-contained Firebase agent for the `firebase_admin_mcp` Django app. This agent includes all necessary components in a single file, making it perfect for standalone deployment, testing, or integration scenarios.

## 🎯 Overview

The Standalone Firebase Agent is based on `firebase_agent_mcp.py` from the main django_firebase_mcp system but is completely independent. It includes:

- **Firebase MCP Client**: Direct communication with Firebase MCP server
- **Agent Configuration**: Complete FA1 agent setup with prompts and parameters
- **State Management**: Firebase-specific state tracking
- **Tool Definitions**: All 14 Firebase tools (Auth, Firestore, Storage)
- **Logging System**: Comprehensive logging with file output
- **Interactive Interface**: Chat-based interaction with the agent

## 📦 What's Included

### Firebase Tools (14 total)

#### Authentication (3 tools)

- `firebase_verify_token`: Verify Firebase ID tokens
- `firebase_create_custom_token`: Create custom authentication tokens
- `firebase_get_user`: Get user information by UID

#### Firestore Database (6 tools)

- `firestore_list_collections`: List all collections
- `firestore_create_document`: Create new documents
- `firestore_get_document`: Retrieve specific documents
- `firestore_update_document`: Update existing documents
- `firestore_delete_document`: Delete documents
- `firestore_query_collection`: Query documents with filters

#### Cloud Storage (4 tools)

- `storage_list_files`: List files with optional prefix filtering
- `storage_upload_file`: Upload files to storage
- `storage_download_file`: Download files from storage
- `storage_delete_file`: Delete files from storage

#### System (1 tool)

- `firebase_health_check`: Check Firebase service health status

## 🚀 Usage

### Method 1: Direct Execution

```bash
cd firebase_admin_mcp
python standalone_firebase_agent.py
```

### Method 2: Django Management Command

```bash
# From Django project root
python manage.py run_standalone_agent

# With custom MCP server URL
python manage.py run_standalone_agent --server-url http://localhost:8002/mcp/
```

### Method 3: Programmatic Usage

```python
from firebase_admin_mcp.standalone_firebase_agent import create_standalone_firebase_agent

# Create agent instance
agent = create_standalone_firebase_agent()

# Use with LangChain/LangGraph
response = agent.invoke({"messages": [HumanMessage(content="List Firebase collections")]})
```

### Method 4: Demo Mode

```bash
cd firebase_admin_mcp
python demo_standalone_agent.py
```

## 🔧 Configuration

The agent uses the following configuration (embedded in the file):

```python
FA1_CONFIG = {
    "name": "Standalone Firebase Agent",
    "model": "gpt-4",
    "temperature": 0.3,
    "max_tokens": 2048,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}
```

### MCP Server Configuration

Default MCP server URL: `http://127.0.0.1:8001/mcp/`

You can customize this by:

- Modifying the `StandaloneFirebaseMCPClient` initialization
- Using the `--server-url` parameter with the Django command
- Setting it programmatically

## 📊 Logging

The agent provides comprehensive logging to `standalone_firebase_agent.log`:

- **Tool Calls**: Every Firebase tool invocation
- **MCP Communication**: Request/response details
- **Performance**: Execution timing measurements
- **Errors**: Detailed error tracking with stack traces
- **Agent Operations**: Agent lifecycle and state changes

## 🛡️ Error Handling

The standalone agent includes robust error handling:

- **MCP Server Connectivity**: Graceful handling of server unavailability
- **Tool Execution Errors**: Detailed error reporting and recovery
- **JSON Parsing**: Safe handling of malformed responses
- **HTTP Errors**: Proper status code and timeout handling
- **User Input**: Validation and sanitization

## 💡 Example Interactions

```
> List all Firestore collections
🤖 I'll list all the Firestore collections for you.
[Lists collections with details...]

> Create a document in the users collection
🤖 I'll create a new document in the users collection. What data would you like to include?

> Check Firebase health status
🤖 Let me check the health status of all Firebase services.
[Shows health check results...]

> Upload a file to Firebase Storage
🤖 I can help you upload a file to Firebase Storage. Please provide the local file path and destination path.
```

## 🔍 State Management

The agent maintains rich state information:

```python
class StandaloneFirebaseState:
    messages: List of conversation messages
    init_run: Initialization flag
    signal: Control signals
    last_operation: Last Firebase operation performed
    firebase_context: {
        "last_query": User's last query
        "response_length": Length of AI response
        "execution_time": Time taken for operation
        "timestamp": Operation timestamp
    }
```

## 🎯 Benefits

### Self-Contained

- No external dependencies on the main django_firebase_mcp system
- All components included in a single file
- Easy to deploy and distribute

### Production-Ready

- Comprehensive logging and monitoring
- Error handling and recovery
- Performance tracking
- Health checking

### Flexible Integration

- Can be used standalone or integrated
- Django management command support
- Programmatic API access
- Demo and testing modes

### Complete Firebase Coverage

- All major Firebase services supported
- Full CRUD operations for Firestore
- Complete storage operations
- Authentication management

## 🧪 Testing

The agent includes a demo script for testing:

```bash
python demo_standalone_agent.py
```

This will:

1. Show all available features
2. List example queries
3. Optionally start the interactive agent

## 📁 Files

- `standalone_firebase_agent.py`: Main agent implementation
- `management/commands/run_standalone_agent.py`: Django management command
- `demo_standalone_agent.py`: Demo and testing script
- `STANDALONE_AGENT.md`: This documentation

## 🔄 Updates

The standalone agent is based on the latest `firebase_agent_mcp.py` implementation and includes all current features. It can be updated independently of the main django_firebase_mcp system.

## 🤝 Integration

While the agent is standalone, it can easily be integrated into larger systems:

- Import the agent creation function
- Use the MCP client directly
- Extend with additional tools
- Customize configuration as needed

The standalone nature makes it perfect for microservices, testing environments, or scenarios where you need Firebase agent capabilities without the full django_firebase_mcp framework.
