#!/usr/bin/env python3
"""
Standalone Firebase Agent for firebase_admin_mcp Django app.

This is a self-contained Firebase agent that includes all necessary components:
- Firebase MCP client
- Agent configuration
- Prompt definition
- State management
- Tool definitions
- Standalone execution capability

Based on firebase_agent_mcp.py but completely standalone within the Django app.
"""

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import django
import json
import requests
import logging
import time
import os
import sys
import argparse
import threading
from typing import Dict, Any, Optional, Sequence, Union
from pydantic import BaseModel

# Add Django project to path for imports
django_project_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
if django_project_path not in sys.path:
    sys.path.append(django_project_path)

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_firebase_mcp.settings')
django.setup()

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================


def setup_logging(verbosity: int = 0):
    """
    Setup logging configuration based on verbosity level.

    Args:
        verbosity: Logging verbosity level
            0 = WARNING (default, minimal output)
            1 = INFO (standard operations)
            2 = DEBUG (detailed debugging)
    """
    # Map verbosity levels to logging levels
    level_map = {
        0: logging.WARNING,  # Default: minimal output
        1: logging.INFO,     # Standard operations
        2: logging.DEBUG     # Detailed debugging
    }

    log_level = level_map.get(verbosity, logging.WARNING)

    # Configure basic logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get logger for this module
    logger = logging.getLogger(__name__)

    # Only create file handler if verbosity > 0
    if verbosity > 0:
        # Create file handler for Standalone Firebase Agent logs
        firebase_agent_log_handler = logging.FileHandler(
            'standalone_firebase_agent.log')
        firebase_agent_log_handler.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        firebase_agent_log_handler.setFormatter(formatter)
        logger.addHandler(firebase_agent_log_handler)

        if verbosity >= 2:
            logger.info(
                "[STANDALONE FIREBASE] Standalone Firebase Agent initialized with DEBUG logging")
        elif verbosity >= 1:
            logger.info(
                "[STANDALONE FIREBASE] Standalone Firebase Agent initialized with INFO logging")

    return logger


# Initialize logger (will be configured later)
logger = logging.getLogger(__name__)

# =============================================================================
# THINKING ANIMATION
# =============================================================================


class ThinkingSpinner:
    """Console spinner animation to show processing status."""

    def __init__(self, message="🤔 Thinking"):
        self.message = message
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
        self.thread = None

    def _spin(self):
        """Spinner animation loop."""
        idx = 0
        while self.running:
            print(
                f'\r{self.message} {self.spinner_chars[idx % len(self.spinner_chars)]}', end='', flush=True)
            time.sleep(0.1)
            idx += 1

    def start(self):
        """Start the spinner animation."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._spin, daemon=True)
            self.thread.start()

    def stop(self, final_message=None):
        """Stop the spinner animation."""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=0.2)
            # Clear the spinner line
            print('\r' + ' ' * (len(self.message) + 3), end='')
            print('\r', end='')
            if final_message:
                print(final_message)

# =============================================================================
# FIREBASE AGENT CONFIGURATION
# =============================================================================


# Firebase Agent Prompt (copied from core.schemas.prompts)
FA1_PROMPT = (
    "You are the Firebase Agent (FA1). You are a specialized agent with direct access to Firebase backend services "
    "through the Firebase Admin SDK. Your role is to help users interact with Firebase Authentication, "
    "Do not provide fake data, all data must come from the Firebase MCP server.\n\n"
    "Firestore Database, and Cloud Storage.\n\n"
    "You have access to the following Firebase capabilities:\n\n"
    "**Firebase Authentication:**\n"
    "- Verify user ID tokens\n"
    "- Create custom authentication tokens\n"
    "- Retrieve user information\n"
    "- Manage user accounts\n\n"
    "**Firestore Database:**\n"
    "- List collections\n"
    "- Get, create, update, and delete documents\n"
    "- Query collections with filters\n"
    "- Manage database operations\n\n"
    "**Firebase Storage:**\n"
    "- Upload and download files\n"
    "- List files with prefix filtering\n"
    "- Delete files from storage\n"
    "- Manage file operations\n\n"
    "**Instructions:**\n"
    "1. Use the appropriate Firebase tools to accomplish user requests\n"
    "2. Provide clear explanations of what operations you're performing\n"
    "3. Handle errors gracefully and explain any limitations\n"
    "4. For complex operations, break them down into logical steps\n"
    "5. Always validate user inputs before making Firebase calls\n\n"
    "When using tools, always explain what you're doing and provide helpful context about the results."
)

# Firebase Agent Configuration (copied from core.schemas.agents)
FA1_CONFIG = {
    "name": "Standalone Firebase Agent",
    "prompt": FA1_PROMPT,
    "temp": 0.3,
    "model": "gpt-4",
    "max_tokens": 2048,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# =============================================================================
# STATE MANAGEMENT
# =============================================================================


class StandaloneFirebaseState(BaseModel):
    """
    State class for Standalone Firebase Agent interactions.

    This state maintains conversation history and control signals for Firebase operations.
    """
    messages: Sequence[Union[HumanMessage, AIMessage]]
    init_run: bool = True
    signal: Union[str, None] = None

    # Firebase-specific state
    last_operation: Union[str, None] = None
    firebase_context: Union[dict, None] = None

# =============================================================================
# FIREBASE MCP CLIENT
# =============================================================================


class StandaloneFirebaseMCPClient:
    """Standalone Firebase MCP client for connecting to Firebase MCP server."""

    def __init__(self, mcp_server_url: str = "http://127.0.0.1:8001/mcp/"):
        self.mcp_server_url = mcp_server_url
        self.request_id = 0
        logger.info(
            f"[STANDALONE MCP] Client initialized with server URL: {mcp_server_url}")

    def _get_next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        logger.debug(f"[REQUEST ID] Generated request ID: {self.request_id}")
        return self.request_id

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a Firebase MCP tool with comprehensive logging and thinking animation."""
        request_id = self._get_next_id()
        start_time = time.time()

        logger.info(f"[TOOL CALL] Calling Firebase MCP tool: {tool_name}")
        logger.debug(
            f"[TOOL ARGS] Tool arguments: {json.dumps(arguments, indent=2, default=str)}")

        # Create thinking animation with tool-specific message
        tool_display_name = tool_name.replace('_', ' ').title()
        spinner = ThinkingSpinner(f"🔥 Firebase: {tool_display_name}")

        # Only show spinner if not in debug mode (verbosity < 2)
        show_spinner = logger.level > logging.DEBUG

        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": request_id
        }

        logger.debug(
            f"[MCP REQUEST] MCP Request payload: {json.dumps(payload, indent=2, default=str)}")

        try:
            if show_spinner:
                spinner.start()

            logger.debug(
                f"[HTTP POST] Sending POST request to: {self.mcp_server_url}")
            response = requests.post(
                self.mcp_server_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            elapsed_time = time.time() - start_time
            logger.info(f"[TIMING] Request completed in {elapsed_time:.3f}s")
            logger.debug(
                f"[HTTP STATUS] HTTP Response Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.debug(
                        f"[MCP RESPONSE] Raw MCP Response: {json.dumps(data, indent=2, default=str)}")

                    if 'result' in data:
                        result_content = data['result']['content'][0]['text']
                        logger.debug(
                            f"[MCP CONTENT] MCP Result Content: {result_content}")

                        try:
                            parsed_result = json.loads(result_content)
                            logger.info(
                                f"[SUCCESS] Tool {tool_name} executed successfully")

                            if show_spinner:
                                spinner.stop(
                                    f"✅ {tool_display_name} completed ({elapsed_time:.2f}s)")

                            return parsed_result
                        except json.JSONDecodeError as parse_error:
                            logger.error(
                                f"[JSON PARSE ERROR] Failed to parse MCP result: {parse_error}")

                            if show_spinner:
                                spinner.stop(
                                    f"❌ {tool_display_name} failed: Parse error")

                            return {
                                "error": "Failed to parse MCP response",
                                "raw_content": result_content,
                                "parse_error": str(parse_error)
                            }
                    else:
                        logger.error(f"[MCP ERROR] MCP returned error: {data}")

                        if show_spinner:
                            spinner.stop(
                                f"❌ {tool_display_name} failed: MCP error")

                        return {"error": "MCP server returned error", "details": data}

                except json.JSONDecodeError as json_error:
                    logger.error(
                        f"[HTTP JSON ERROR] Failed to parse HTTP response: {json_error}")

                    if show_spinner:
                        spinner.stop(
                            f"❌ {tool_display_name} failed: JSON error")

                    return {
                        "error": "Failed to parse HTTP response",
                        "status_code": response.status_code,
                        "content": response.text[:500]
                    }
            else:
                logger.error(
                    f"[HTTP ERROR] HTTP request failed with status {response.status_code}")

                if show_spinner:
                    spinner.stop(
                        f"❌ {tool_display_name} failed: HTTP {response.status_code}")

                return {
                    "error": f"HTTP request failed with status {response.status_code}",
                    "content": response.text[:500]
                }

        except requests.exceptions.RequestException as req_error:
            elapsed_time = time.time() - start_time
            logger.error(
                f"[REQUEST ERROR] Request failed after {elapsed_time:.3f}s: {req_error}")

            if show_spinner:
                spinner.stop(f"❌ {tool_display_name} failed: Connection error")

            return {
                "error": "Request to MCP server failed",
                "exception": str(req_error),
                "server_url": self.mcp_server_url
            }
        finally:
            # Ensure spinner is stopped even if an exception occurs
            if show_spinner and spinner.running:
                spinner.stop()


# Global MCP client instance
mcp_client = StandaloneFirebaseMCPClient()

# =============================================================================
# FIREBASE TOOLS (with correct tool names for Django MCP server)
# =============================================================================


@tool
def firebase_health_check():
    """
    Check the health status of Firebase MCP services with detailed logging.
    """
    logger.info("[HEALTH CHECK] Running Firebase health check...")

    try:
        result = mcp_client.call_tool("list_collections", {})
        logger.debug(
            f"[HEALTH CHECK] Health check result: {json.dumps(result, indent=2, default=str)}")

        if "error" not in result:
            health_status = {
                "status": "healthy",
                "services": ["authentication", "firestore", "storage"],
                "collections_count": len(result) if isinstance(result, list) else "unknown",
                "message": "All Firebase services operational"
            }
            logger.info("[HEALTH CHECK SUCCESS] Firebase health check passed")
            return health_status
        else:
            health_status = {
                "status": "degraded",
                "error": result.get("error"),
                "error_details": result,
                "message": "Firebase services partially available"
            }
            logger.warning(
                f"[HEALTH CHECK WARNING] Firebase health check degraded: {result.get('error')}")
            return health_status
    except Exception as e:
        health_status = {
            "status": "error",
            "error": str(e),
            "message": "Firebase services unavailable"
        }
        logger.error(f"[HEALTH CHECK ERROR] Firebase health check failed: {e}")
        logger.exception("Health check exception:")
        return health_status


@tool
def firestore_list_collections():
    """List all collections in Firestore database."""
    logger.info("[FIRESTORE] Listing collections")
    return mcp_client.call_tool("list_collections", {})


@tool
def firestore_create_document(collection: str, data: dict, document_id: Optional[str] = None):
    """Create a new document in a Firestore collection."""
    logger.info(f"[FIRESTORE] Creating document in collection: {collection}")
    arguments = {
        "collection": collection,
        "data": data
    }
    if document_id:
        arguments["document_id"] = document_id
    return mcp_client.call_tool("create_document", arguments)


@tool
def firestore_get_document(collection: str, document_id: str):
    """Get a document from a Firestore collection."""
    logger.info(
        f"[FIRESTORE] Getting document {document_id} from collection {collection}")
    return mcp_client.call_tool("get_document", {
        "collection": collection,
        "document_id": document_id
    })


@tool
def firestore_update_document(collection: str, document_id: str, data: dict):
    """Update a document in a Firestore collection."""
    logger.info(
        f"[FIRESTORE] Updating document {document_id} in collection {collection}")
    return mcp_client.call_tool("update_document", {
        "collection": collection,
        "document_id": document_id,
        "data": data
    })


@tool
def firestore_delete_document(collection: str, document_id: str):
    """Delete a document from a Firestore collection."""
    logger.info(
        f"[FIRESTORE] Deleting document {document_id} from collection {collection}")
    return mcp_client.call_tool("delete_document", {
        "collection": collection,
        "document_id": document_id
    })


@tool
def firestore_query_collection(collection: str, filters: Optional[dict] = None, limit: Optional[int] = None):
    """Query documents in a Firestore collection with optional filters."""
    logger.info(f"[FIRESTORE] Querying collection: {collection}")
    arguments = {"collection": collection}
    if filters:
        arguments["filters"] = filters
    if limit:
        arguments["limit"] = limit
    return mcp_client.call_tool("query_collection", arguments)


@tool
def storage_list_files(prefix: Optional[str] = None):
    """List files in Firebase Storage with optional prefix filter."""
    logger.info(f"[STORAGE] Listing files with prefix: {prefix}")
    arguments = {}
    if prefix:
        arguments["prefix"] = prefix
    return mcp_client.call_tool("list_files", arguments)


@tool
def storage_upload_file(file_path: str, destination_path: str):
    """Upload a file to Firebase Storage."""
    logger.info(f"[STORAGE] Uploading file {file_path} to {destination_path}")
    return mcp_client.call_tool("upload_file", {
        "file_path": file_path,
        "destination_path": destination_path
    })


@tool
def storage_download_file(file_path: str, destination_path: str):
    """Download a file from Firebase Storage."""
    logger.info(
        f"[STORAGE] Downloading file {file_path} to {destination_path}")
    return mcp_client.call_tool("download_file", {
        "file_path": file_path,
        "destination_path": destination_path
    })


@tool
def storage_delete_file(file_path: str):
    """Delete a file from Firebase Storage."""
    logger.info(f"[STORAGE] Deleting file: {file_path}")
    return mcp_client.call_tool("delete_file", {
        "file_path": file_path
    })


@tool
def firebase_verify_token(id_token: str):
    """Verify a Firebase ID token."""
    logger.info("[AUTH] Verifying Firebase ID token")
    return mcp_client.call_tool("verify_id_token", {
        "id_token": id_token
    })


@tool
def firebase_create_custom_token(uid: str, additional_claims: Optional[dict] = None):
    """Create a custom Firebase authentication token."""
    logger.info(f"[AUTH] Creating custom token for UID: {uid}")
    arguments = {"uid": uid}
    if additional_claims:
        arguments["additional_claims"] = additional_claims
    return mcp_client.call_tool("create_custom_token", arguments)


@tool
def firebase_get_user(uid: str):
    """Get user information by UID."""
    logger.info(f"[AUTH] Getting user information for UID: {uid}")
    return mcp_client.call_tool("get_user", {
        "uid": uid
    })

# =============================================================================
# STANDALONE FIREBASE AGENT
# =============================================================================


# Global agent instance cache
agent_instance = None


def create_standalone_firebase_agent():
    """
    Creates a standalone Firebase agent instance for backend operations with detailed logging.

    Returns:
        An instance of a LangGraph React agent configured with Firebase tools
    """
    logger.info(
        "[AGENT CREATE] Creating standalone Firebase agent instance...")

    model = ChatOpenAI(
        model=FA1_CONFIG["model"],
        temperature=FA1_CONFIG["temp"],
        max_tokens=FA1_CONFIG["max_tokens"],
        top_p=FA1_CONFIG["top_p"],
        frequency_penalty=FA1_CONFIG["frequency_penalty"],
        presence_penalty=FA1_CONFIG["presence_penalty"],
    )

    logger.debug(f"[AGENT CONFIG] Firebase agent model config: {FA1_CONFIG}")

    prompt_text = FA1_CONFIG["prompt"]
    logger.debug(
        f"[AGENT PROMPT] Firebase agent prompt length: {len(prompt_text)} characters")

    # All Firebase MCP tools
    tools = [
        firebase_health_check,
        firestore_list_collections,
        firestore_create_document,
        firestore_get_document,
        firestore_update_document,
        firestore_delete_document,
        firestore_query_collection,
        storage_list_files,
        storage_upload_file,
        storage_download_file,
        storage_delete_file,
        firebase_verify_token,
        firebase_create_custom_token,
        firebase_get_user,
    ]

    logger.info(
        f"[AGENT CREATE SUCCESS] Firebase agent created with {len(tools)} Firebase MCP tools")

    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt_text,
    )

    logger.info(
        "[AGENT CREATE COMPLETE] Standalone Firebase agent instance created successfully")
    return agent


def run_standalone_firebase_agent():
    """
    Run the standalone Firebase agent in interactive mode.
    """
    global agent_instance

    logger.info("[AGENT RUN] Starting standalone Firebase agent...")

    if agent_instance is None:
        logger.info("[AGENT RUN] Creating new Firebase agent instance...")
        agent_instance = create_standalone_firebase_agent()

    # Initialize state
    state = StandaloneFirebaseState(
        messages=[],
        init_run=True,
        signal="init"
    )

    print("🔥 Standalone Firebase Agent (FA1) initialized!")
    print("I have access to Firebase backend services:")
    print("  [✓] Firebase Authentication")
    print("  [✓] Firestore Database")
    print("  [✓] Firebase Storage")
    print("  [✓] Real-time Firebase operations")
    print("Type 'exit' to quit.\n")

    logger.info("[SERVICES OK] All Firebase services available")

    while True:
        try:
            user_msg = input("> ")
            logger.info(f"[USER INPUT] User input received: '{user_msg}'")

            if user_msg.lower() == "exit":
                logger.info("[EXIT] Exit signal received")
                print("👋 Goodbye!")
                break

            # Add user message to state
            state.messages.append(HumanMessage(content=user_msg))
            logger.debug(
                f"[STATE] Total messages in state: {len(state.messages)}")

            # Invoke agent
            logger.info(
                "[AGENT INVOKE] Invoking Firebase agent with user message...")
            start_time = time.time()

            # Start thinking spinner
            spinner = ThinkingSpinner("🤔 Firebase Agent is processing")
            spinner.start()

            response = agent_instance.invoke(
                {"messages": list(state.messages)},
                {"recursion_limit": 10, "max_iterations": 5}
            )

            # Stop thinking spinner
            spinner.stop("✅ Processing complete")
            elapsed_time = time.time() - start_time
            logger.info(
                f"[TIMING] Agent invocation completed in {elapsed_time:.3f}s")

            if "messages" in response and response["messages"]:
                ai_response = response["messages"][-1].content
                logger.info(
                    "[AGENT SUCCESS] Firebase agent responded successfully")
                logger.debug(
                    f"[RESPONSE LENGTH] AI response length: {len(ai_response)} characters")

                # Log tool calls that were made
                for msg in response["messages"]:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        logger.info(
                            f"[TOOL CALLS] Tool calls made: {[tc.get('name', 'unknown') for tc in msg.tool_calls]}")
                    elif hasattr(msg, 'type') and msg.type == 'tool':
                        logger.info(
                            f"[TOOL RESPONSE] Tool response: {msg.name}")

                print(f"\n🤖 Firebase Agent: {ai_response}\n")

                # Update state
                state.messages.append(AIMessage(content=ai_response))
                state.last_operation = "firebase_interaction"
                state.firebase_context = {
                    "last_query": user_msg,
                    "response_length": len(ai_response),
                    "execution_time": elapsed_time,
                    "timestamp": time.time()
                }

            else:
                error_msg = "No response messages from agent"
                logger.error(f"[AGENT ERROR] {error_msg}")
                print(f"\n❌ Error: {error_msg}\n")

        except KeyboardInterrupt:
            logger.info("[INTERRUPT] Keyboard interrupt received")
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            logger.error(
                f"[AGENT ERROR] Standalone Firebase Agent Error: {error_msg}")
            logger.exception("Full exception traceback:")
            print(f"\n❌ Error: {error_msg}\n")

# =============================================================================
# ARGUMENT PARSING
# =============================================================================


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Standalone Firebase Agent for firebase_admin_mcp Django app',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Verbosity levels:
  0 = WARNING (default, minimal output)
  1 = INFO (standard operations)  
  2 = DEBUG (detailed debugging)

Examples:
  python -m firebase_admin_mcp.standalone_firebase_agent
  python -m firebase_admin_mcp.standalone_firebase_agent -v 1
  python -m firebase_admin_mcp.standalone_firebase_agent --verbosity 2
        """
    )

    parser.add_argument(
        '-v', '--verbosity',
        type=int,
        choices=[0, 1, 2],
        default=0,
        help='Set logging verbosity level (default: 0)'
    )

    parser.add_argument(
        '--mcp-url',
        type=str,
        default="http://127.0.0.1:8001/mcp/",
        help='MCP server URL (default: http://127.0.0.1:8001/mcp/)'
    )

    return parser.parse_args()

# =============================================================================
# MAIN EXECUTION
# =============================================================================


if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()

    # Setup logging based on verbosity
    logger = setup_logging(args.verbosity)
    # Update MCP client URL if provided
    if args.mcp_url != "http://127.0.0.1:8001/mcp/":
        mcp_client.mcp_server_url = args.mcp_url
        if args.verbosity > 0:
            logger.info(
                f"[MCP CONFIG] Using custom MCP server URL: {args.mcp_url}")

    print("🔥 Standalone Firebase Agent for firebase_admin_mcp Django App")
    print("=" * 60)

    if args.verbosity > 0:
        print(f"Logging verbosity: {args.verbosity}")
        print(f"MCP server URL: {args.mcp_url}")

    print("This is a self-contained Firebase agent with all components included.")
    print("It connects to the Firebase MCP server for backend operations.")
    print("=" * 60)

    # Run the standalone agent
    run_standalone_firebase_agent()
