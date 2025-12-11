"""
Test Step 7a: Verify Cognito OAuth Setup
========================================
Run: python lab/tests/test_step7a.py
"""

import sys
import inspect
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step7a():
    """Test that Step 7a is correctly implemented."""
    print("=" * 60)
    print("Testing Step 7a: Cognito OAuth Setup")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step7a_cognito_oauth import (
            create_cognito_user_pool,
            create_cognito_domain,
            create_resource_server,
            create_app_client,
            get_access_token,
            cleanup_cognito
        )
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check boto3 import
    print("\n[Test 2] Checking boto3 import in module...")
    try:
        import lab.exercises.step7a_cognito_oauth as module
        source = inspect.getsource(module)
        if "import boto3" not in source:
            print("  ✗ boto3 not imported")
            print("  Hint: Complete TODO 1 - import boto3")
            return False
        print("  ✓ boto3 imported")
    except Exception as e:
        print(f"  ✗ Could not check imports: {e}")

    # Test 3: Check create_cognito_user_pool implementation
    print("\n[Test 3] Checking create_cognito_user_pool implementation...")
    source = inspect.getsource(create_cognito_user_pool)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ create_cognito_user_pool() not implemented")
        print("  Hint: Complete TODO 2 - use cognito.create_user_pool()")
        return False
    required = ["create_user_pool", "PoolName"]
    missing = [r for r in required if r not in source]
    if missing:
        print(f"  ⚠ Might be missing: {missing}")
    else:
        print("  ✓ create_cognito_user_pool() implemented")

    # Test 4: Check create_cognito_domain implementation
    print("\n[Test 4] Checking create_cognito_domain implementation...")
    source = inspect.getsource(create_cognito_domain)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ create_cognito_domain() not implemented")
        print("  Hint: Complete TODO 3 - use cognito.create_user_pool_domain()")
        return False
    if "create_user_pool_domain" not in source:
        print("  ⚠ Should call create_user_pool_domain()")
    else:
        print("  ✓ create_cognito_domain() implemented")

    # Test 5: Check create_resource_server implementation
    print("\n[Test 5] Checking create_resource_server implementation...")
    source = inspect.getsource(create_resource_server)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ create_resource_server() not implemented")
        print("  Hint: Complete TODO 4 - use cognito.create_resource_server()")
        return False
    required = ["create_resource_server", "Scopes"]
    missing = [r for r in required if r not in source]
    if missing:
        print(f"  ⚠ Might be missing: {missing}")
    else:
        print("  ✓ create_resource_server() implemented")

    # Test 6: Check create_app_client implementation
    print("\n[Test 6] Checking create_app_client implementation...")
    source = inspect.getsource(create_app_client)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ create_app_client() not implemented")
        print("  Hint: Complete TODO 5 - use cognito.create_user_pool_client()")
        return False
    required = ["create_user_pool_client", "client_credentials", "GenerateSecret"]
    missing = [r for r in required if r not in source]
    if missing:
        print(f"  ⚠ Might be missing: {missing}")
        print("  Hint: M2M auth requires GenerateSecret=True and AllowedOAuthFlows=['client_credentials']")
    else:
        print("  ✓ create_app_client() implemented correctly")

    # Test 7: Check get_access_token implementation
    print("\n[Test 7] Checking get_access_token implementation...")
    source = inspect.getsource(get_access_token)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ get_access_token() not implemented")
        print("  Hint: Complete TODO 6 - POST to /oauth2/token endpoint")
        return False
    required = ["oauth2/token", "client_credentials", "base64", "Authorization"]
    missing = [r for r in required if r not in source]
    if missing:
        print(f"  ⚠ Might be missing: {missing}")
    else:
        print("  ✓ get_access_token() implemented correctly")

    # Test 8: Check cleanup_cognito implementation
    print("\n[Test 8] Checking cleanup_cognito implementation...")
    source = inspect.getsource(cleanup_cognito)
    if "pass" in source and source.strip().endswith("pass"):
        print("  ✗ cleanup_cognito() not implemented")
        print("  Hint: Complete TODO 7 - delete domain and user pool")
        return False
    required = ["delete_user_pool_domain", "delete_user_pool"]
    missing = [r for r in required if r not in source]
    if missing:
        print(f"  ⚠ Might be missing: {missing}")
    else:
        print("  ✓ cleanup_cognito() implemented")

    # Test 9: Check for existing config (optional live test)
    print("\n[Test 9] Checking for existing Cognito configuration...")
    try:
        from lab.exercises.step7a_cognito_oauth import load_cognito_config
        config = load_cognito_config()
        print(f"  ✓ Found existing config!")
        print(f"    Pool ID: {config['pool_id']}")
        print(f"    Domain: {config['domain']}")
        print(f"    Token URL: {config['token_url']}")

        # Try to get a token
        print("\n[Test 10] Testing live token generation...")
        try:
            token = get_access_token(
                config['domain'],
                config['region'],
                config['client_id'],
                config['client_secret']
            )
            if token:
                print(f"  ✓ Successfully obtained access token!")
                print(f"    Token preview: {token[:40]}...")
        except Exception as e:
            print(f"  ⚠ Could not get token: {e}")

    except FileNotFoundError:
        print("  ℹ No existing config found")
        print("  Run the exercise to create Cognito resources:")
        print("    python lab/exercises/step7a_cognito_oauth.py")

    print("\n" + "=" * 60)
    print("Step 7a Code Review PASSED!")
    print("=" * 60)
    print("""
Your code is correctly structured. To fully test:

1. Run the exercise to create Cognito resources:
   python lab/exercises/step7a_cognito_oauth.py

2. This will create:
   - Cognito User Pool
   - OAuth Domain
   - Resource Server with scopes
   - App Client for M2M auth
   - Test token generation

3. Then proceed to Step 7b:
   python lab/exercises/step7b_gateway_auth.py

4. Clean up when completely done:
   python lab/exercises/step7a_cognito_oauth.py --cleanup
""")
    return True


if __name__ == "__main__":
    success = test_step7a()
    sys.exit(0 if success else 1)
