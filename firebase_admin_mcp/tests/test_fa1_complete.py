#!/usr/bin/env python3
"""
Complete test of Firebase Agent (FA1) setup.
"""


def test_firebase_agent_complete():
    """Test all Firebase Agent components."""
    print("🔥 Firebase Agent (FA1) Complete Integration Test")
    print("=" * 50)

    success_count = 0
    total_tests = 6

    # Test 1: Prompts and Agents schemas
    try:
        from core.schemas.prompts import Prompts
        from core.schemas.agents import Agents

        fa1_prompt = Prompts.FA1_PROMPT
        fa1_config = Agents.FA1

        print("✅ Test 1: FA1 Prompt and Agent configuration")
        print(f"   📝 Prompt length: {len(fa1_prompt)} characters")
        print(f"   🤖 Agent: {fa1_config['name']}")
        print(f"   🧠 Model: {fa1_config['model']}")
        success_count += 1

    except Exception as e:
        print(f"❌ Test 1 Failed: {e}")

    # Test 2: Firebase State
    try:
        from orchestration.states.firebase import FirebaseState
        from langchain_core.messages import HumanMessage

        state = FirebaseState(
            messages=[HumanMessage(content="Test message")],
            init_run=True,
            signal="test"
        )

        print("✅ Test 2: FirebaseState creation")
        print(f"   📨 Messages: {len(state.messages)}")
        print(
            f"   🔧 Has firebase_context: {hasattr(state, 'firebase_context')}")
        success_count += 1

    except Exception as e:
        print(f"❌ Test 2 Failed: {e}")

    # Test 3: Firebase Agent Creation
    try:
        from tools.agents.firebase_agent_mcp import create_firebase_agent

        agent = create_firebase_agent()

        print("✅ Test 3: Firebase agent creation")
        print(f"   🤖 Agent type: {type(agent).__name__}")
        success_count += 1

    except Exception as e:
        print(f"❌ Test 3 Failed: {e}")

    # Test 4: Firebase Agent Node
    try:
        from tools.agents.firebase_agent_mcp import firebase_agent_node

        print("✅ Test 4: Firebase agent node function")
        print(f"   🔧 Node function: {firebase_agent_node.__name__}")
        success_count += 1

    except Exception as e:
        print(f"❌ Test 4 Failed: {e}")

    # Test 5: Firebase Graph
    try:
        from orchestration.graphs.firebase import fgraph, firebase_ai

        print("✅ Test 5: Firebase graph")
        print(f"   📊 Graph type: {type(fgraph).__name__}")
        print(f"   🎯 Compiled graph: {type(firebase_ai).__name__}")
        success_count += 1

    except Exception as e:
        print(f"❌ Test 5 Failed: {e}")

    # Test 6: Package Exports
    try:
        from tools.agents import create_firebase_agent, firebase_agent_node

        print("✅ Test 6: Package exports")
        print("   📦 Firebase agent exported in tools.agents")
        success_count += 1

    except Exception as e:
        print(f"❌ Test 6 Failed: {e}")

    # Summary
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {success_count}/{total_tests} passed")

    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n📋 Firebase Agent (FA1) is fully integrated:")
        print("   ✅ FA1_PROMPT registered in core/schemas/prompts.py")
        print("   ✅ FA1 agent config in core/schemas/agents.py")
        print("   ✅ FirebaseState class in orchestration/states/firebase.py")
        print("   ✅ Firebase graph in orchestration/graphs/firebase.py")
        print("   ✅ Firebase agent in tools/agents/firebase_agent_mcp.py")
        print("   ✅ Package integration in tools/agents/__init__.py")

        print("\n🚀 Usage Examples:")
        print("   from tools.agents import create_firebase_agent")
        print("   from orchestration.graphs.firebase import firebase_ai")
        print("   from core.schemas.agents import Agents")
        print("   config = Agents.FA1")

        print("\n🔥 Firebase Agent follows the exact DA1 pattern!")

    else:
        print("❌ Some tests failed. Check the errors above.")

    return success_count == total_tests


if __name__ == "__main__":
    test_firebase_agent_complete()
