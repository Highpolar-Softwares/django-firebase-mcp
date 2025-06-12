#!/usr/bin/env python3
"""
Demo script showing how to use the Firebase-enhanced dummy agent.
This demonstrates the agent using real Firebase tools instead of dummy tools.
"""
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def demo_standalone_firebase_agent():
    """Demo the standalone Firebase agent."""
    print("=== Firebase Agent Demo ===\n")

    try:
        from tools.agents.firebase_agent import create_firebase_agent
        from langchain_core.messages import HumanMessage

        print("Creating Firebase agent...")
        agent = create_firebase_agent()
        print("✅ Firebase agent created!\n")

        # Demo queries
        demo_queries = [
            "What collections are available in the Firestore database?",
            "Create a test document in a collection called 'demo_collection' with some sample data",
            "List the files in Firebase Storage",
        ]

        print("Demo queries you could ask:")
        for i, query in enumerate(demo_queries, 1):
            print(f"  {i}. {query}")

        print("\n(Note: Would need OpenAI API key to run actual queries)")

    except Exception as e:
        print(f"❌ Error creating Firebase agent: {e}")


def demo_enhanced_dummy_agent():
    """Demo the enhanced dummy agent with Firebase tools."""
    print("\n=== Enhanced Dummy Agent Demo ===\n")

    try:
        from tools.agents.dummy_agent import create_dummy_agent, FIREBASE_AVAILABLE

        print(f"Firebase Available: {FIREBASE_AVAILABLE}")

        if FIREBASE_AVAILABLE:
            print("✅ Your dummy agent now has Firebase superpowers!")
            print("\nYour agent can now:")
            print("  🔥 Access real Firestore collections")
            print("  🔥 Create and retrieve documents")
            print("  🔥 List files in Firebase Storage")
            print("  🔍 Still perform dummy searches")

            agent = create_dummy_agent()
            print("\n✅ Enhanced dummy agent created successfully!")

        else:
            print("📝 Firebase not available - using standard dummy tools")

    except Exception as e:
        print(f"❌ Error creating enhanced dummy agent: {e}")


def show_usage_examples():
    """Show usage examples."""
    print("\n" + "="*60)
    print("🚀 How to Use Your Firebase-Enhanced Agent")
    print("="*60)

    print("\n1. **Direct Firebase Agent Usage:**")
    print("```python")
    print("from tools.agents.firebase_agent import create_firebase_agent")
    print("from langchain_core.messages import HumanMessage")
    print("")
    print("agent = create_firebase_agent()")
    print("response = agent.invoke({")
    print(
        "    'messages': [HumanMessage(content='List Firestore collections')]")
    print("})")
    print("```")

    print("\n2. **Enhanced Dummy Agent (Auto-detects Firebase):**")
    print("```python")
    print("from tools.agents.dummy_agent import create_dummy_agent")
    print("")
    print("# Automatically uses Firebase tools if available")
    print("agent = create_dummy_agent()")
    print("```")

    print("\n3. **Individual Firebase Tools:**")
    print("```python")
    print("from tools.agents.firebase_mcp_client import (")
    print("    firestore_list_collections,")
    print("    firestore_create_document,")
    print("    storage_list_files")
    print(")")
    print("")
    print("# Use tools directly")
    print("collections = firestore_list_collections.invoke({})")
    print("```")

    print("\n4. **State-based Agent Node (LangGraph):**")
    print("```python")
    print("from tools.agents.firebase_agent import firebase_agent_node")
    print("from orchestration.states.dummy import DummyState")
    print("from orchestration.graphs.base import SIGNALS")
    print("")
    print("# Use in LangGraph workflow")
    print("state = DummyState(signal=SIGNALS.INIT, messages=[])")
    print("new_state = firebase_agent_node(state)")
    print("```")


def main():
    """Run the demo."""
    print("🔥 Firebase MCP + LangChain Agent Integration Demo")
    print("="*60)

    # Check prerequisites
    try:
        import requests
        response = requests.get("http://127.0.0.1:8001/mcp/", timeout=5)
        if response.status_code != 200:
            print("❌ Firebase MCP server not running properly")
            print("   Start it with: python manage.py runserver 8001")
            return
    except:
        print("❌ Firebase MCP server not running")
        print("   Start it with: python manage.py runserver 8001")
        return

    print("✅ Firebase MCP server is running")

    # Run demos
    demo_standalone_firebase_agent()
    demo_enhanced_dummy_agent()
    show_usage_examples()

    print("\n" + "="*60)
    print("🎯 Integration Complete!")
    print("="*60)
    print("Your dummy agent now has access to:")
    print("  🔥 Firebase Authentication (4 tools)")
    print("  🔥 Firestore Database (6 tools)")
    print("  🔥 Firebase Storage (4 tools)")
    print("  📋 Total: 14 Firebase MCP tools available!")
    print("\nThe agent will automatically use Firebase tools when available,")
    print("and fall back to dummy tools when Firebase is not accessible.")


if __name__ == "__main__":
    main()
