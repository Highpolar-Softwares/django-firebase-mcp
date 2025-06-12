#!/usr/bin/env python3
"""
Demo script for the Standalone Firebase Agent in firebase_admin_mcp Django app.

This script demonstrates how to use the standalone Firebase agent that includes
all necessary components without external dependencies on the main django_firebase_mcp system.
"""

import os
import sys

# Add the project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


def demo_standalone_firebase_agent():
    """Demo the standalone Firebase agent functionality."""
    print("🔥 Standalone Firebase Agent Demo")
    print("=" * 50)

    print("This demo shows the capabilities of the standalone Firebase agent.")
    print("The agent includes all components in a single file:\n")

    print("📦 Components included:")
    print("  ✓ Firebase MCP Client")
    print("  ✓ Agent Configuration (FA1)")
    print("  ✓ Firebase Prompt Definition")
    print("  ✓ State Management")
    print("  ✓ All Firebase Tools (14 tools)")
    print("  ✓ Comprehensive Logging")
    print("  ✓ Interactive Chat Interface")

    print("\n🛠️ Available Firebase Tools:")
    print("  Authentication:")
    print("    - firebase_verify_token")
    print("    - firebase_create_custom_token")
    print("    - firebase_get_user")

    print("  Firestore Database:")
    print("    - firestore_list_collections")
    print("    - firestore_create_document")
    print("    - firestore_get_document")
    print("    - firestore_update_document")
    print("    - firestore_delete_document")
    print("    - firestore_query_collection")

    print("  Cloud Storage:")
    print("    - storage_list_files")
    print("    - storage_upload_file")
    print("    - storage_download_file")
    print("    - storage_delete_file")

    print("  System:")
    print("    - firebase_health_check")

    print("\n🚀 Usage Options:")
    print("1. Run directly:")
    print("   python firebase_admin_mcp/standalone_firebase_agent.py")

    print("\n2. Run via Django management command:")
    print("   python manage.py run_standalone_agent")

    print("\n3. Import and use programmatically:")
    print("   from firebase_admin_mcp.standalone_firebase_agent import create_standalone_firebase_agent")
    print("   agent = create_standalone_firebase_agent()")

    print("\n4. Run with custom MCP server URL:")
    print("   python manage.py run_standalone_agent --server-url http://localhost:8002/mcp/")

    print("\n📋 Features:")
    print("  🔍 Comprehensive logging to 'standalone_firebase_agent.log'")
    print("  🛡️ Error handling and recovery")
    print("  ⚡ Performance timing measurements")
    print("  🎯 Tool call tracking")
    print("  💾 State management with Firebase context")
    print("  🔄 Interactive chat loop")
    print("  🌐 MCP protocol compliance")

    print("\n✨ Try these example queries:")
    examples = [
        "List all Firestore collections",
        "Check Firebase health status",
        "Create a new document in the 'users' collection",
        "List all files in Firebase Storage",
        "Get user information for a specific UID",
        "Query documents in a collection with filters"
    ]

    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")

    print("\n" + "=" * 50)
    print("🎯 The standalone agent is completely self-contained!")
    print("   All dependencies are included in the single file.")
    print("   Perfect for deployment, testing, or standalone use.")
    print("=" * 50)

    # Ask if user wants to run the agent
    print("\n💡 Would you like to start the interactive agent now? (y/n)")
    choice = input("> ").lower().strip()

    if choice in ['y', 'yes']:
        print("\n🚀 Starting Standalone Firebase Agent...")
        print("(Use Ctrl+C to exit)")

        try:
            from firebase_admin_mcp.standalone_firebase_agent import run_standalone_firebase_agent
            run_standalone_firebase_agent()
        except KeyboardInterrupt:
            print("\n👋 Demo completed!")
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Make sure you're running this from the Django project root.")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("👋 Demo completed! Run the agent anytime using the methods above.")


if __name__ == "__main__":
    demo_standalone_firebase_agent()
