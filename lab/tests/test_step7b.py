"""
Test Step 7b: Verify Gateway + OAuth Setup
==========================================
Run: python lab/tests/test_step7b.py
"""

import sys
import inspect
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step7b():
    """Test that Step 7b is correctly implemented."""
    print("=" * 60)
    print("Testing Step 7b: Gateway with Your Cognito OAuth")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step7b_gateway_auth import (
            create_gateway_with_cognito,
            add_lambda_target,
            create_authenticated_agent,
            cleanup_gateway,
            load_cognito_config
        )
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check boto3 import
    print("\n[Test 2] Checking boto3 import in module...")
    try:
        import lab.exercises.step7b_gateway_auth as module
        source = inspect.getsource(module)
        if "import boto3" not in source:
            print("  ✗ boto3 not imported")
            print("  Hint: Complete TODO 1 - import boto3")
            return False
        print("  ✓ boto3 imported")
    except Exception as e:
        print(f"  ✗ Could not check imports: {e}")

    # Test 3: Check create_gateway_with_cognito implementation
    print("\n[Test 3] Checking create_gateway_with_cognito implementation...")
    source = inspect.getsource(create_gateway_with_cognito)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ create_gateway_with_cognito() not implemented")
        print("  Hint: Complete TODO 2 - use boto3 bedrock-agentcore-control client")
        return False
    required = ["create_gateway", "CUSTOM_JWT", "discoveryUrl"]
    missing = [r for r in required if r not in source]
    if missing:
        print(f"  ⚠ Might be missing: {missing}")
    else:
        print("  ✓ create_gateway_with_cognito() implemented")

    # Test 4: Check add_lambda_target implementation
    print("\n[Test 4] Checking add_lambda_target implementation...")
    source = inspect.getsource(add_lambda_target)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ add_lambda_target() not implemented")
        print("  Hint: Complete TODO 3 - use create_target()")
        return False
    if "create_target" not in source:
        print("  ⚠ Should call create_target()")
    else:
        print("  ✓ add_lambda_target() implemented")

    # Test 5: Check create_authenticated_agent implementation
    print("\n[Test 5] Checking create_authenticated_agent implementation...")
    source = inspect.getsource(create_authenticated_agent)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ create_authenticated_agent() not implemented")
        print("  Hint: Complete TODO 4 - create MCPClient with Bearer token")
        return False
    required = ["MCPClient", "Bearer", "Authorization"]
    missing = [r for r in required if r not in source]
    if missing:
        print(f"  ⚠ Might be missing: {missing}")
    else:
        print("  ✓ create_authenticated_agent() implemented correctly")

    # Test 6: Check cleanup_gateway implementation
    print("\n[Test 6] Checking cleanup_gateway implementation...")
    source = inspect.getsource(cleanup_gateway)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ cleanup_gateway() not implemented")
        print("  Hint: Complete TODO 5 - use delete_gateway()")
        return False
    if "delete_gateway" not in source:
        print("  ⚠ Should call delete_gateway()")
    else:
        print("  ✓ cleanup_gateway() implemented")

    # Test 7: Check for Cognito config (prerequisite)
    print("\n[Test 7] Checking for Cognito config from Step 7a...")
    cognito_config = load_cognito_config()
    if cognito_config is None:
        print("  ✗ cognito_config.json not found")
        print("  You must complete Step 7a first!")
        print("    python lab/exercises/step7a_cognito_oauth.py")
        return False
    print(f"  ✓ Found Cognito config")
    print(f"    Pool ID: {cognito_config['pool_id']}")
    print(f"    Domain: {cognito_config['domain']}")

    # Test 8: Check for existing Gateway config
    print("\n[Test 8] Checking for Gateway configuration...")
    try:
        from lab.exercises.step7b_gateway_auth import load_gateway_config
        gateway_config = load_gateway_config()
        print(f"  ✓ Found existing Gateway!")
        print(f"    Gateway ID: {gateway_config['gateway_id']}")
        print(f"    Gateway URL: {gateway_config['gateway_url'][:50]}...")

        # Test 9: Try to get token and connect
        print("\n[Test 9] Testing live connection...")
        try:
            from lab.exercises.step7b_gateway_auth import get_access_token
            token = get_access_token(cognito_config)
            print(f"  ✓ Got access token from YOUR Cognito")

            mcp_client, model = create_authenticated_agent(
                gateway_config['gateway_url'],
                token,
                gateway_config['region']
            )
            print(f"  ✓ Created authenticated agent")

        except Exception as e:
            print(f"  ⚠ Could not test live connection: {e}")

    except FileNotFoundError:
        print("  ℹ No existing Gateway config found")
        print("  Run the exercise to create Gateway:")
        print("    python lab/exercises/step7b_gateway_auth.py")

    print("\n" + "=" * 60)
    print("Step 7b Code Review PASSED!")
    print("=" * 60)
    print("""
Your code is correctly structured. To fully test:

1. Make sure Step 7a is complete (cognito_config.json exists)

2. Run the exercise to create Gateway:
   python lab/exercises/step7b_gateway_auth.py

3. This will:
   - Load YOUR Cognito config
   - Create Gateway with YOUR Cognito as auth
   - Get token from YOUR Cognito
   - Connect agent with Bearer token
   - Test authenticated access

4. Clean up when done:
   python lab/exercises/step7b_gateway_auth.py --cleanup
   python lab/exercises/step7a_cognito_oauth.py --cleanup
""")
    return True


if __name__ == "__main__":
    success = test_step7b()
    sys.exit(0 if success else 1)
