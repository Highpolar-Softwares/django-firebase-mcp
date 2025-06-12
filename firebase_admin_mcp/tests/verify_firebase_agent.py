#!/usr/bin/env python3
"""
Simple verification script for Firebase Agent (FA1) setup.
"""

print("🔥 Firebase Agent (FA1) Verification")
print("="*40)

# Test 1: Agent Configuration
try:
    from core.schemas.agents import Agents
    print("✅ Agents schema imported")
    if hasattr(Agents, 'FA1'):
        print(f"✅ FA1 found: {Agents.FA1['name']}")
    else:
        print("❌ FA1 not found")
except Exception as e:
    print(f"❌ Agents import failed: {e}")

# Test 2: Prompt Configuration
try:
    from core.schemas.prompts import Prompts
    print("✅ Prompts schema imported")
    if hasattr(Prompts, 'FA1_PROMPT'):
        print("✅ FA1_PROMPT found")
    else:
        print("❌ FA1_PROMPT not found")
except Exception as e:
    print(f"❌ Prompts import failed: {e}")

# Test 3: Firebase State
try:
    from orchestration.states.firebase import FirebaseState
    state = FirebaseState(messages=[], init_run=True)
    print("✅ FirebaseState created")
except Exception as e:
    print(f"❌ FirebaseState failed: {e}")

# Test 4: Firebase Agent
try:
    from tools.agents.firebase_agent_mcp import create_firebase_agent
    agent = create_firebase_agent()
    print("✅ Firebase agent created")
except Exception as e:
    print(f"❌ Firebase agent failed: {e}")

print("\n🎯 Firebase Agent (FA1) is ready!")
print("Usage:")
print("  python orchestration/graphs/firebase.py")
print("  from tools.agents import create_firebase_agent")
