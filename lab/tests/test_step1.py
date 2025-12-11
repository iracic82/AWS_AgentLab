"""
Test Step 1: Verify Hello World Agent
=====================================
Run: python lab/tests/test_step1.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_step1():
    """Test that Step 1 is correctly implemented."""
    print("=" * 60)
    print("Testing Step 1: Hello World Agent")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step1_hello_agent import create_agent
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        print("  Hint: Make sure you added the import statements")
        return False

    # Test 2: Check agent is created
    print("\n[Test 2] Checking agent creation...")
    try:
        agent = create_agent()
        if agent is None:
            print("  ✗ Agent is None - complete the TODOs!")
            return False
        print("  ✓ Agent created successfully")
    except Exception as e:
        print(f"  ✗ Agent creation failed: {e}")
        return False

    # Test 3: Check agent can respond
    print("\n[Test 3] Checking agent can respond...")
    try:
        response = agent("Say 'hello' and nothing else")
        if response is None:
            print("  ✗ Agent returned None")
            return False
        print(f"  ✓ Agent responded: {str(response)[:50]}...")
    except Exception as e:
        print(f"  ✗ Agent invocation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("Step 1 PASSED! You can proceed to Step 2.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_step1()
    sys.exit(0 if success else 1)
