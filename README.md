# Django Firebase MCP

A comprehensive Django app that implements Firebase Model Context Protocol (MCP) server, enabling AI agents to interact with Firebase services through a standardized protocol.

## 🚀 Quick Start

Get up and running in under 5 minutes with the standalone Firebase agent for testing.

### Prerequisites

- Python 3.11+
- Firebase project with Admin SDK
- Git (optional)

### 1. Clone & Setup

```bash
git clone https://github.com/your-repo/django-firebase-mcp.git
cd django-firebase-mcp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Firebase Setup

#### Get Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (or create a new one)
3. Navigate to **Project Settings** → **Service Accounts**
4. Click **"Generate new private key"**
5. Download the JSON file and save it as `credentials.json` in the project root

#### Enable Firebase Services

Make sure these services are enabled in your Firebase project:

- **Authentication** (for user management)
- **Firestore Database** (for document storage)
- **Cloud Storage** (for file uploads)

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Firebase Configuration
SERVICE_ACCOUNT_KEY_PATH=credentials.json
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com

# MCP Configuration
MCP_TRANSPORT=http
MCP_HOST=127.0.0.1
MCP_PORT=8001

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

**⚠️ Important:** Replace `your-project-id` with your actual Firebase project ID.

### 5. Quick Test with Standalone Agent

Test your setup immediately with the standalone Firebase agent:

```bash
# Run the standalone agent
python firebase_admin_mcp/standalone_firebase_agent.py
```

You should see:

```
🔥 Firebase MCP Agent Ready!
Type 'help' for available commands, 'quit' to exit.

>
```

Try these commands:

```
> List all Firebase collections
> Check Firebase health status
> help
> quit
```

### 6. Full Django Setup (Optional)

For full Django integration:

```bash
# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run Django development server
python manage.py runserver 8001
```

The MCP server will be available at: `http://127.0.0.1:8001/mcp/`

## 🛠️ Management Commands

### Core Commands

```bash
# Run standalone Firebase agent (quick testing)
python firebase_admin_mcp/standalone_firebase_agent.py

# Run MCP server via Django
python manage.py runserver 8001

# Run MCP server in stdio mode (for MCP clients)
python manage.py run_mcp --transport stdio

# Run MCP server in HTTP mode
python manage.py run_mcp --transport http --host 127.0.0.1 --port 8001

# Run standalone agent via Django management command
python manage.py run_standalone_agent
```

### Testing Commands

```bash
# Test Firebase connectivity
python firebase_admin_mcp/tests/test_firebase_connection.py

# Test MCP server completeness
python firebase_admin_mcp/tests/test_mcp_complete.py

# Demo Firebase agent
python firebase_admin_mcp/tests/demo_firebase_agent.py

# Demo standalone agent
python firebase_admin_mcp/demo_standalone_agent.py
```

## 🔧 Available Tools

The MCP server provides **14 Firebase tools** across three categories:

### 🔐 Authentication (4 tools)

- `firebase_verify_token` - Verify Firebase ID tokens
- `firebase_create_custom_token` - Create custom auth tokens
- `firebase_get_user` - Get user info by UID
- `firebase_delete_user` - Delete user accounts

### 📚 Firestore Database (6 tools)

- `firestore_list_collections` - List all collections
- `firestore_create_document` - Create new documents
- `firestore_get_document` - Retrieve documents
- `firestore_update_document` - Update documents
- `firestore_delete_document` - Delete documents
- `firestore_query_collection` - Query with filters

### 🗄️ Cloud Storage (4 tools)

- `storage_list_files` - List files with filtering
- `storage_upload_file` - Upload files
- `storage_download_file` - Download files
- `storage_delete_file` - Delete files

## 🧪 Quick Testing

### Test Server Health

```bash
curl http://127.0.0.1:8001/mcp/
```

### Test a Firebase Tool

```bash
curl -X POST http://127.0.0.1:8001/mcp/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "firestore_list_collections",
      "arguments": {}
    },
    "id": 1
  }'
```

## 🤖 AI Agent Integration

### LangChain Example

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Import Firebase tools
from firebase_admin_mcp.tools.agents.firebase_mcp_client import ALL_FIREBASE_TOOLS

# Create agent with Firebase capabilities
model = ChatOpenAI(model="gpt-4")
agent = create_react_agent(
    model=model,
    tools=ALL_FIREBASE_TOOLS,
    prompt="You are a Firebase assistant with full database and storage access."
)

# Use the agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "Show me all my Firestore collections"}]
})
```

## 📚 Documentation

This project includes comprehensive documentation:

- **[FIREBASE_ADMIN_MCP.md](FIREBASE_ADMIN_MCP.md)** - Complete technical documentation

  - Detailed API reference
  - All tool specifications
  - Advanced configuration
  - Security considerations
  - Production deployment guide

- **[STANDALONE_AGENT.md](STANDALONE_AGENT.md)** - Standalone agent documentation
  - Self-contained Firebase agent
  - Complete feature overview
  - Usage examples
  - Integration patterns

## 🔧 Troubleshooting

### Common Issues

**Problem:** `Default app does not exist` error
**Solution:** Verify `credentials.json` path in `.env` file

**Problem:** Server won't start
**Solution:** Check if port 8001 is available: `netstat -an | findstr :8001`

**Problem:** Firebase connection fails
**Solution:** Verify Firebase services are enabled in console

**Problem:** Import errors
**Solution:** Ensure all dependencies installed: `pip install -r requirements.txt`

## 🎯 What's Next?

1. **Explore the Standalone Agent** - Perfect for quick testing and demos
2. **Read the Full Documentation** - See FIREBASE_ADMIN_MCP.md for complete details
3. **Integrate with Your AI Agents** - Use the MCP tools in your applications
4. **Customize for Your Needs** - Extend with additional Firebase operations

## 📝 Project Structure

```
django-firebase-mcp/
├── README.md                          # This file
├── FIREBASE_ADMIN_MCP.md             # Complete documentation
├── STANDALONE_AGENT.md               # Standalone agent guide
├── requirements.txt                   # Python dependencies
├── credentials.json                   # Firebase credentials (you create this)
├── .env                              # Environment variables (you create this)
├── manage.py                         # Django management
├── firebase_admin_mcp/               # Main MCP app
│   ├── standalone_firebase_agent.py  # Standalone agent
│   ├── tools/                        # Firebase MCP tools
│   ├── management/commands/          # Django commands
│   └── tests/                        # Test suite
└── django_firebase_mcp/             # Django project settings
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**🔥 Ready to supercharge your AI agents with Firebase?**

Start with the standalone agent, then explore the full documentation for advanced usage!
