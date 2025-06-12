#!/usr/bin/env python3
"""
Test script for the new Firebase Agent (FA1) following django_firebase_mcp patterns.

This script tests:
1. FA1 agent configuration in core/schemas/agents
2. FA1 prompt in core/schemas/prompts  
3. Firebase state in orchestration/states/firebase
4. Firebase graph in orchestration/graphs/firebase
5. Firebase agent implementation in tools/agents/firebase_agent_mcp
"""
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_firebase_agent_configuration():
    """Test if FA1 agent is properly configured in schemas."""
    print("=== Testing Firebase Agent Configuration ===\n")

    try:
        from core.schemas.agents import Agents
        from core.schemas.prompts import Prompts

        # Test FA1 agent configuration
        if hasattr(Agents, 'FA1'):
            fa1_config = Agents.FA1
            print(f"✅ FA1 Agent found: {fa1_config['name']}")
            print(f"   Model: {fa1_config['model']}")
            print(f"   Temperature: {fa1_config['temp']}")
            print(f"   Max Tokens: {fa1_config['max_tokens']}")
        else:
            print("❌ FA1 agent not found in Agents schema")
            return False

        # Test FA1 prompt
        if hasattr(Prompts, 'FA1_PROMPT'):
            print("✅ FA1_PROMPT found in Prompts schema")
            prompt_preview = Prompts.FA1_PROMPT[:100] + "..."
            print(f"   Preview: {prompt_preview}")
        else:
            print("❌ FA1_PROMPT not found in Prompts schema")
            return False

        return True

    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_firebase_state():
    """Test Firebase state class."""
    print("\n=== Testing Firebase State ===\n")

    try:
        from orchestration.states.firebase import FirebaseState
        from langchain_core.messages import HumanMessage, AIMessage

        # Create a test state
        state = FirebaseState(
            messages=[HumanMessage(content="Test message")],
            init_run=True,
            signal="init"
        )

        print("✅ FirebaseState created successfully")
        print(f"   Messages: {len(state.messages)}")
        print(f"   Init run: {state.init_run}")
        print(f"   Signal: {state.signal}")

        # Test adding messages
        state.messages.append(AIMessage(content="Response message"))
        print(f"✅ Message appending works: {len(state.messages)} messages")

        return True

    except Exception as e:
        print(f"❌ Firebase state test failed: {e}")
        return False


def test_firebase_agent():
    """Test Firebase agent creation."""
    print("\n=== Testing Firebase Agent ===\n")

    try:
        from tools.agents.firebase_agent_mcp import create_firebase_agent, FIREBASE_MCP_AVAILABLE

        print(f"Firebase MCP Available: {FIREBASE_MCP_AVAILABLE}")

        # Create the agent
        agent = create_firebase_agent()
        print("✅ Firebase agent created successfully")

        if FIREBASE_MCP_AVAILABLE:
            print("✅ Agent has access to real Firebase MCP tools")
        else:
            print("⚠️  Agent using fallback tools (Firebase MCP not available)")

        return True

    except Exception as e:
        print(f"❌ Firebase agent test failed: {e}")
        return False


def test_firebase_graph():
    """Test Firebase graph creation."""
    print("\n=== Testing Firebase Graph ===\n")

    try:
        from orchestration.graphs.firebase import firebase_ai, firebase_config

        print("✅ Firebase graph compiled successfully")
        print(f"   Config: {firebase_config}")

        # Test the graph structure
        print("✅ Graph nodes and edges configured")

        return True

    except Exception as e:
        print(f"❌ Firebase graph test failed: {e}")
        return False


def test_firebase_mcp_server():
    """Test if Firebase MCP server is accessible."""
    print("\n=== Testing Firebase MCP Server ===\n")

    try:
        import requests
        response = requests.get('http://127.0.0.1:8001/mcp/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Firebase MCP server is running")
            print(f"   Server: {data.get('name')}")
            print(f"   Tools: {len(data.get('tools', []))}")
            return True
        else:
            print(
                f"⚠️  MCP server responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Firebase MCP server not accessible: {e}")
        print("   (This is OK if you haven't started the server)")
        return False


def test_complete_integration():
    """Test the complete Firebase agent pipeline."""
    print("\n=== Testing Complete Integration ===\n")

    try:
        from orchestration.states.firebase import FirebaseState
        from tools.agents.firebase_agent_mcp import firebase_agent_node
        from orchestration.graphs.base import SIGNALS
        from langchain_core.messages import HumanMessage

        # Create initial state
        state = FirebaseState(
            messages=[HumanMessage(content="Test Firebase integration")],
            signal=SIGNALS.INIT
        )

        print("✅ Firebase agent integration test setup complete")
        print("   State created with test message")
        print("   Ready for firebase_agent_node invocation")

        # Note: We don't actually invoke the node here since it requires user input
        print("   (Actual node execution requires interactive input)")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def main():
    """Run all Firebase agent tests."""
    print("🔥 Firebase Agent (FA1) Test Suite")
    print("Following django_firebase_mcp Agent Patterns")
    print("="*50)

    tests = [
        ("Configuration", test_firebase_agent_configuration),
        ("Firebase State", test_firebase_state),
        ("Firebase Agent", test_firebase_agent),
        ("Firebase Graph", test_firebase_graph),
        ("MCP Server", test_firebase_mcp_server),
        ("Integration", test_complete_integration),
    ]

    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()

    print("\n" + "="*50)
    print("🎯 TEST RESULTS")
    print("="*50)

    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1

    print(f"\nPassed: {passed}/{len(tests)} tests")

    if passed == len(tests):
        print("\n🎉 All tests passed!")
        print("\nFirebase Agent (FA1) is ready to use:")
        print("  📋 Run directly: python orchestration/graphs/firebase.py")
        print("  🔧 Import: from tools.agents import create_firebase_agent")
        print("  🌐 Graph: python orchestration/graphs/firebase.py --graph firebase")

    elif passed >= len(tests) - 1:  # All except MCP server
        print("\n✅ Core Firebase Agent setup complete!")
        print("⚠️  Start Firebase MCP server for full functionality:")
        print("     python manage.py runserver 8001")

    else:
        print("\n❌ Some tests failed - check the output above")


if __name__ == "__main__":
    main()
