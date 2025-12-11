"""
Test Step 3: Verify AWS Status Tool Implementation
==================================================
Run: python lab/tests/test_step3.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step3():
    """Test that Step 3 is correctly implemented."""
    print("=" * 60)
    print("Testing Step 3: AWS Status Tool")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step3_aws_status_tool import check_aws_status, create_agent_with_both_tools
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check @tool decorator is applied
    print("\n[Test 2] Checking @tool decorator...")
    tool_attrs = ['name', 'description', '__call__', '__wrapped__']
    is_tool = any(hasattr(check_aws_status, attr) for attr in tool_attrs)
    if not is_tool:
        print("  ✗ @tool decorator not applied")
        print("  Hint: Add @tool above the function definition")
        return False
    print("  ✓ @tool decorator applied")

    # Test 3: Test the tool directly
    print("\n[Test 3] Testing tool with 'us-west-2'...")
    try:
        result = check_aws_status("us-west-2")
        if isinstance(result, dict):
            if result.get("status"):
                print(f"  ✓ Got status: {result['status']} - {result.get('message', '')[:50]}")
            else:
                print("  ✗ Tool returned empty data")
                print(f"  Result was: {result}")
                print("  Hint: Check your TODO 5")
                return False
        else:
            print(f"  ✗ Tool should return dict, got: {type(result)}")
            return False
    except Exception as e:
        print(f"  ✗ Tool call failed: {e}")
        print("  Hint: Check your HTTP request in TODO 2")
        return False

    # Test 4: Check required fields
    print("\n[Test 4] Checking returned fields...")
    required_fields = ["region", "status", "message", "recommendation"]
    missing = [f for f in required_fields if f not in result]
    if missing:
        print(f"  ✗ Missing fields: {missing}")
        print("  Hint: Make sure TODO 5 returns all required fields")
        return False
    print(f"  ✓ All required fields present")

    # Test 5: Check status value is valid
    print("\n[Test 5] Checking status values...")
    valid_statuses = ["healthy", "check_needed", "unknown"]
    if result.get("status") not in valid_statuses:
        print(f"  ✗ Invalid status: {result.get('status')}")
        print(f"  Valid statuses: {valid_statuses}")
        return False
    print(f"  ✓ Valid status returned: {result.get('status')}")

    # Test 6: Check agent with both tools
    print("\n[Test 6] Checking agent with both tools...")
    try:
        agent = create_agent_with_both_tools()
        if agent is None:
            print("  ✗ Agent is None")
            print("  Hint: Complete TODO 6")
            return False

        print(f"  ✓ Agent created with tools")
    except Exception as e:
        print(f"  ✗ Agent creation failed: {e}")
        return False

    # Test 7: Agent uses tools
    print("\n[Test 7] Testing agent uses both tools...")
    try:
        response = agent("Check us-east-1 status and weather in Virginia")
        print(f"  ✓ Agent responded successfully")
    except Exception as e:
        print(f"  ✗ Agent invocation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("Step 3 PASSED! You can proceed to Step 4.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_step3()
    sys.exit(0 if success else 1)
