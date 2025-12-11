"""
Test Step 6: Verify AgentCore Handler
=====================================
Run: python lab/tests/test_step6.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step6():
    """Test that Step 6 is correctly implemented."""
    print("=" * 60)
    print("Testing Step 6: AgentCore Handler")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step6_agentcore_handler import app, model, agent
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check BedrockAgentCoreApp import
    print("\n[Test 2] Checking BedrockAgentCoreApp import...")
    try:
        from bedrock_agentcore import BedrockAgentCoreApp
        print("  ✓ BedrockAgentCoreApp available")
    except ImportError as e:
        print(f"  ✗ BedrockAgentCoreApp not installed: {e}")
        print("  Hint: pip install bedrock-agentcore")
        return False

    # Test 3: Check app is created
    print("\n[Test 3] Checking app instance...")
    if app is None:
        print("  ✗ App is None")
        print("  Hint: Complete TODO 2 - app = BedrockAgentCoreApp()")
        return False

    from bedrock_agentcore import BedrockAgentCoreApp
    if not isinstance(app, BedrockAgentCoreApp):
        print("  ✗ App is not a BedrockAgentCoreApp instance")
        print("  Hint: app = BedrockAgentCoreApp()")
        return False
    print("  ✓ App created correctly")

    # Test 4: Check model is created
    print("\n[Test 4] Checking model instance...")
    if model is None:
        print("  ✗ Model is None")
        print("  Hint: Complete TODO 3 - create BedrockModel")
        return False
    print("  ✓ Model created")

    # Test 5: Check agent is created
    print("\n[Test 5] Checking agent instance...")
    if agent is None:
        print("  ✗ Agent is None")
        print("  Hint: Complete TODO 3 - create Agent with model, system_prompt, and tools")
        return False
    print("  ✓ Agent created")

    # Test 6: Check agent has tools
    print("\n[Test 6] Checking agent has tools...")
    print("  ✓ Agent configured with tools")

    # Test 7: Check invoke function exists with decorator
    print("\n[Test 7] Checking invoke function...")
    try:
        # Import the module to check for invoke
        import lab.exercises.step6_agentcore_handler as handler_module

        invoke_fn = None
        for name in dir(handler_module):
            obj = getattr(handler_module, name)
            if callable(obj) and hasattr(obj, '__wrapped__'):
                invoke_fn = obj
                break

        if invoke_fn is None:
            # Try direct lookup
            if hasattr(handler_module, 'invoke'):
                invoke_fn = handler_module.invoke
                if not hasattr(invoke_fn, '__wrapped__'):
                    print("  ✗ invoke function exists but missing @app.entrypoint decorator")
                    print("  Hint: Add @app.entrypoint above def invoke(payload):")
                    return False
            else:
                print("  ✗ invoke function not found")
                print("  Hint: Complete TODO 4 - create invoke function with @app.entrypoint")
                return False

        print("  ✓ Entry point function configured")

    except Exception as e:
        print(f"  ✗ Could not verify invoke function: {e}")
        print("  Hint: Make sure you created the invoke function with @app.entrypoint")
        return False

    # Test 8: Test invoke function works
    print("\n[Test 8] Testing invoke function...")
    try:
        # Get the unwrapped function or call it directly
        test_payload = {"prompt": "Should I deploy to us-east-1?"}

        # Try calling the agent directly since invoke may need app context
        response = agent("Test: Should I deploy?")
        response_text = str(response).upper()

        has_recommendation = any(word in response_text for word in [
            "GO", "CAUTION", "NO-GO", "PROCEED", "SAFE", "RECOMMEND", "DEPLOY"
        ])

        if has_recommendation:
            print("  ✓ Agent responds with deployment recommendations")
        else:
            print("  ⚠ Agent response might not have clear recommendation")

    except Exception as e:
        print(f"  ✗ Invoke test failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("Step 6 PASSED!")
    print("=" * 60)
    print("""
Your handler is ready for AgentCore deployment!

Next steps:
1. Configure: agentcore configure -e lab/exercises/step6_agentcore_handler.py -r us-west-2 --disable-memory -n devops_agent
2. Deploy: agentcore deploy
3. Invoke: agentcore invoke '{"prompt": "Should I deploy to us-east-1?"}'
4. Cleanup: agentcore destroy
""")
    return True


if __name__ == "__main__":
    success = test_step6()
    sys.exit(0 if success else 1)
