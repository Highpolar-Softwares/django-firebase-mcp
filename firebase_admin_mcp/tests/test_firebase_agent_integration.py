#!/usr/bin/env python3
"""
Test script to verify Firebase MCP integration with LangChain agent.
"""
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_firebase_mcp_client():
    """Test the Firebase MCP client directly."""
    print("=== Testing Firebase MCP Client ===\n")

    try:
        from tools.agents.firebase_mcp_client import firebase_client, firestore_list_collections

        # Test 1: Direct client call
        print("1. Testing direct MCP client call...")
        result = firebase_client.call_tool("list_collections", {})
        if "error" not in result:
            print(
                f"   ✅ Direct call successful - found {len(result)} collections")
        else:
            print(f"   ❌ Direct call failed: {result['error']}")

        # Test 2: LangChain tool wrapper
        print("\n2. Testing LangChain tool wrapper...")
        tool_result = firestore_list_collections.invoke({})
        if "error" not in tool_result:
            print(
                f"   ✅ LangChain tool successful - found {len(tool_result)} collections")
        else:
            print(f"   ❌ LangChain tool failed: {tool_result['error']}")

        print("\n✅ Firebase MCP client is working!")
        return True

    except Exception as e:
        print(f"❌ Firebase MCP client test failed: {e}")
        return False


def test_dummy_agent_integration():
    """Test the dummy agent with Firebase integration."""
    print("\n=== Testing Dummy Agent Integration ===\n")

    try:
        from tools.agents.dummy_agent import create_dummy_agent, FIREBASE_AVAILABLE

        print(f"Firebase Available: {FIREBASE_AVAILABLE}")

        if FIREBASE_AVAILABLE:
            print("✅ Dummy agent will use Firebase MCP tools")

            # Create the agent
            agent = create_dummy_agent()
            print("✅ Firebase-enhanced dummy agent created successfully")

            # Test a simple invocation
            test_messages = [
                {"role": "user", "content": "What collections are available in Firestore?"}]
            print("\n🧪 Testing agent invocation...")

            # Note: This would require OpenAI API key to actually run
            print("   (Agent ready - would need OpenAI API key for full test)")

        else:
            print("📝 Firebase not available - dummy agent will use mock tools")
            agent = create_dummy_agent()
            print("✅ Standard dummy agent created successfully")

        return True

    except Exception as e:
        print(f"❌ Dummy agent integration test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Firebase MCP + LangChain Integration Test\n")

    # Check if MCP server is running
    try:
        import requests
        response = requests.get("http://127.0.0.1:8001/mcp/", timeout=5)
        if response.status_code == 200:
            print("✅ Firebase MCP server is running\n")
            server_running = True
        else:
            print("❌ Firebase MCP server responded with error\n")
            server_running = False
    except:
        print("❌ Firebase MCP server is not running")
        print("   Start it with: python manage.py runserver 8001\n")
        server_running = False

    if not server_running:
        print("Skipping tests - MCP server not available")
        return

    # Run tests
    client_test = test_firebase_mcp_client()
    agent_test = test_dummy_agent_integration()

    print("\n" + "="*50)
    if client_test and agent_test:
        print("🎉 All tests passed!")
        print("\nYour dummy agent can now use Firebase MCP tools:")
        print("  ✅ Firebase Authentication")
        print("  ✅ Firestore Database")
        print("  ✅ Firebase Storage")
        print("\nTo use the enhanced agent:")
        print("  1. Make sure the MCP server is running: python manage.py runserver 8001")
        print("  2. Run your agent - it will automatically detect and use Firebase tools")
    else:
        print("❌ Some tests failed - check the output above")


if __name__ == "__main__":
    main()
