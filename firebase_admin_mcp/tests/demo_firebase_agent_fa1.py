#!/usr/bin/env python3
"""
Demo script for the new Firebase Agent (FA1).
This shows how to use the Firebase agent following the same pattern as dummy_agent.
"""


def demo_firebase_agent_setup():
    """Demo the Firebase agent setup and usage."""
    print("🔥 Firebase Agent (FA1) Demo")
    print("=" * 40)

    # 1. Test imports
    print("\n1. Testing imports...")
    try:
        from core.schemas.prompts import Prompts
        from core.schemas.agents import Agents
        from orchestration.states.firebase import FirebaseState
        from tools.agents.firebase_agent_mcp import create_firebase_agent, firebase_agent_node
        print("   ✅ All imports successful")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return

    # 2. Test FA1 configuration
    print("\n2. Testing FA1 configuration...")
    try:
        fa1_config = Agents.FA1
        print(f"   ✅ FA1 Agent: {fa1_config['name']}")
        print(f"   🤖 Model: {fa1_config['model']}")
        print(f"   🌡️  Temperature: {fa1_config['temp']}")
    except Exception as e:
        print(f"   ❌ Config error: {e}")
        return

    # 3. Test agent creation
    print("\n3. Testing agent creation...")
    try:
        agent = create_firebase_agent()
        print("   ✅ Firebase agent created successfully")
        print(f"   🔧 Agent type: {type(agent).__name__}")
    except Exception as e:
        print(f"   ❌ Agent creation error: {e}")
        return

    # 4. Test state creation
    print("\n4. Testing state creation...")
    try:
        from langchain_core.messages import HumanMessage
        state = FirebaseState(
            messages=[HumanMessage(content="Hello Firebase!")],
            init_run=True,
            signal="init"
        )
        print("   ✅ FirebaseState created successfully")
        print(f"   📝 Messages: {len(state.messages)}")
        print(f"   🔧 Firebase context: {hasattr(state, 'firebase_context')}")
    except Exception as e:
        print(f"   ❌ State creation error: {e}")
        return

    # 5. Test graph setup
    print("\n5. Testing graph setup...")
    try:
        from orchestration.graphs.firebase import fgraph, firebase_ai
        print("   ✅ Firebase graph imported successfully")
        print(f"   📊 Graph type: {type(fgraph).__name__}")
        print(f"   🤖 Compiled graph: {type(firebase_ai).__name__}")
    except Exception as e:
        print(f"   ❌ Graph error: {e}")
        return

    print("\n" + "=" * 40)
    print("🎉 Firebase Agent (FA1) Setup Complete!")
    print("=" * 40)

    print("\n📋 Summary of what was created:")
    print("   ✅ FA1_PROMPT in core.schemas.prompts")
    print("   ✅ FA1 agent config in core.schemas.agents")
    print("   ✅ FirebaseState class in orchestration.states.firebase")
    print("   ✅ Firebase graph in orchestration.graphs.firebase")
    print("   ✅ Firebase agent in tools.agents.firebase_agent_mcp")

    print("\n🚀 Usage Examples:")
    print("\n1. Create Firebase agent directly:")
    print("   from tools.agents.firebase_agent_mcp import create_firebase_agent")
    print("   agent = create_firebase_agent()")

    print("\n2. Use in LangGraph workflow:")
    print("   from tools.agents import firebase_agent_node")
    print("   from orchestration.states.firebase import FirebaseState")

    print("\n3. Run Firebase graph:")
    print("   python orchestration/graphs/firebase.py --graph firebase")

    print("\n4. Access FA1 configuration:")
    print("   from core.schemas.agents import Agents")
    print("   config = Agents.FA1")

    print("\n🔥 The Firebase Agent follows the exact same pattern as the Dummy Agent!")
    print("   - Registered in core/schemas/agents.py as FA1")
    print("   - Prompt defined in core/schemas/prompts.py as FA1_PROMPT")
    print("   - State class in orchestration/states/firebase.py")
    print("   - Graph in orchestration/graphs/firebase.py")
    print("   - Agent implementation in tools/agents/firebase_agent_mcp.py")


if __name__ == "__main__":
    demo_firebase_agent_setup()
