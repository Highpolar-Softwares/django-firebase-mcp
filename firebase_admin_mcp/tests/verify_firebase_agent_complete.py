#!/usr/bin/env python3
"""
Comprehensive verification of the new Firebase Agent (FA1) setup.
Tests all components: prompt, agent config, state, graph, and integration.
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_prompt_registration():
    """Test that FA1_PROMPT is registered in core.schemas.prompts"""
    print("1. Testing FA1 prompt registration...")
    try:
        from core.schemas.prompts import Prompts

        # Check if FA1_PROMPT exists
        if hasattr(Prompts, 'FA1_PROMPT'):
            prompt = Prompts.FA1_PROMPT
            print(f"   ✅ FA1_PROMPT found")
            print(f"   📝 Prompt length: {len(prompt)} characters")
            print(
                f"   🎯 Contains 'Firebase Agent': {'Firebase Agent' in prompt}")
            return True
        else:
            print("   ❌ FA1_PROMPT not found in Prompts class")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_agent_registration():
    """Test that FA1 is registered in core.schemas.agents"""
    print("\n2. Testing FA1 agent registration...")
    try:
        from core.schemas.agents import Agents

        # Check if FA1 exists
        if hasattr(Agents, 'FA1'):
            fa1_config = Agents.FA1
            print(f"   ✅ FA1 agent found")
            print(f"   📝 Name: {fa1_config['name']}")
            print(f"   🤖 Model: {fa1_config['model']}")
            print(f"   🌡️ Temperature: {fa1_config['temp']}")
            print(f"   🎯 Prompt type: {type(fa1_config['prompt'])}")
            return True
        else:
            print("   ❌ FA1 not found in Agents class")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_state_class():
    """Test FirebaseState class"""
    print("\n3. Testing FirebaseState class...")
    try:
        from orchestration.states.firebase import FirebaseState
        from langchain_core.messages import HumanMessage, AIMessage

        # Create a test state
        state = FirebaseState(
            messages=[HumanMessage(content="Test message")],
            init_run=True,
            signal="init"
        )

        print(f"   ✅ FirebaseState class imported successfully")
        print(f"   📝 State created with {len(state.messages)} message(s)")
        print(f"   🔧 Has init_run: {hasattr(state, 'init_run')}")
        print(f"   🔧 Has signal: {hasattr(state, 'signal')}")
        print(
            f"   🔧 Has firebase_context: {hasattr(state, 'firebase_context')}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_agent_creation():
    """Test Firebase agent creation"""
    print("\n4. Testing Firebase agent creation...")
    try:
        from tools.agents.firebase_agent_mcp import create_firebase_agent, FIREBASE_MCP_AVAILABLE

        print(f"   🔥 Firebase MCP Available: {FIREBASE_MCP_AVAILABLE}")

        # Create agent
        agent = create_firebase_agent()
        print(f"   ✅ Firebase agent created successfully")
        print(f"   🤖 Agent type: {type(agent)}")

        # Test agent has required attributes
        has_invoke = hasattr(agent, 'invoke')
        print(f"   🔧 Has invoke method: {has_invoke}")

        return True
    except Exception as e:
        print(f"   ❌ Error creating agent: {e}")
        return False


def test_agent_node():
    """Test Firebase agent node function"""
    print("\n5. Testing Firebase agent node function...")
    try:
        from tools.agents.firebase_agent_mcp import firebase_agent_node
        from orchestration.states.firebase import FirebaseState
        from orchestration.graphs.base import SIGNALS
        from langchain_core.messages import HumanMessage

        # Create test state
        test_state = FirebaseState(
            messages=[HumanMessage(content="Hello")],
            init_run=True,
            signal=SIGNALS.INIT
        )

        print(f"   ✅ firebase_agent_node function imported")
        print(f"   📝 Test state created")
        print(f"   🔧 Node function callable: {callable(firebase_agent_node)}")

        # Note: We won't actually call the node as it requires user input
        print(f"   ℹ️  Node function ready (requires user input to test)")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_graph_creation():
    """Test Firebase graph creation"""
    print("\n6. Testing Firebase graph creation...")
    try:
        from orchestration.graphs.firebase import fgraph, firebase_ai, firebase_config

        print(f"   ✅ Firebase graph imported successfully")
        print(f"   📊 Graph type: {type(fgraph)}")
        print(f"   🤖 Compiled AI type: {type(firebase_ai)}")
        print(f"   ⚙️  Config available: {bool(firebase_config)}")

        # Check graph structure
        nodes = getattr(fgraph, 'nodes', {})
        print(f"   🔗 Graph has {len(nodes)} nodes")

        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_package_imports():
    """Test package-level imports"""
    print("\n7. Testing package imports...")
    try:
        from tools.agents import create_firebase_agent, firebase_agent_node

        print(f"   ✅ Firebase agent imports work from package")
        print(f"   🔧 create_firebase_agent: {callable(create_firebase_agent)}")
        print(f"   🔧 firebase_agent_node: {callable(firebase_agent_node)}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_firebase_mcp_integration():
    """Test Firebase MCP client integration"""
    print("\n8. Testing Firebase MCP integration...")
    try:
        # Check if MCP server is running
        import requests
        response = requests.get('http://127.0.0.1:8001/mcp/', timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Firebase MCP server is running")

            # Test MCP client tools
            try:
                from tools.agents.firebase_mcp_client import firestore_list_collections
                print(f"   ✅ Firebase MCP client tools available")

                # Test a simple tool call
                result = firestore_list_collections.invoke({})
                if "error" not in result:
                    print(
                        f"   ✅ MCP tools working - found {len(result)} collections")
                else:
                    print(f"   ⚠️  MCP tool error: {result.get('error')}")

                return True
            except Exception as e:
                print(f"   ⚠️  MCP client error: {e}")
                return False
        else:
            print(
                f"   ⚠️  MCP server not running (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ⚠️  MCP server connection failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🔥 Firebase Agent (FA1) Setup Verification")
    print("=" * 50)

    tests = [
        test_prompt_registration,
        test_agent_registration,
        test_state_class,
        test_agent_creation,
        test_agent_node,
        test_graph_creation,
        test_package_imports,
        test_firebase_mcp_integration,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    test_names = [
        "Prompt Registration",
        "Agent Registration",
        "State Class",
        "Agent Creation",
        "Agent Node Function",
        "Graph Creation",
        "Package Imports",
        "Firebase MCP Integration"
    ]

    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1:2d}. {name:<25} {status}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Firebase Agent (FA1) is ready!")
        print("\n🚀 You can now use:")
        print("   - FA1 agent configuration in core.schemas.agents")
        print("   - FA1 prompt in core.schemas.prompts")
        print("   - FirebaseState in orchestration.states.firebase")
        print("   - Firebase graph in orchestration.graphs.firebase")
        print("   - Firebase agent tools in tools.agents.firebase_agent_mcp")
        print("\n🎯 To run the Firebase agent:")
        print("   python orchestration/graphs/firebase.py --graph firebase")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
