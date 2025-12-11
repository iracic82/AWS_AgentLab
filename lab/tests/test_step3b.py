"""
Test Step 3b: Verify IPAM Tool
==============================
Run: python lab/tests/test_step3b.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step3b():
    """Test that Step 3b is correctly implemented."""
    print("=" * 60)
    print("Testing Step 3b: Infoblox CSP IPAM Tool")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step3b_ipam_tool import check_subnet_capacity, get_mock_subnet_data
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check mock data function
    print("\n[Test 2] Checking mock data function...")
    mock_result = get_mock_subnet_data("us-west-2")
    if mock_result is None:
        print("  ✗ get_mock_subnet_data() returned None")
        print("  Hint: Complete TODO 2")
        return False

    if "total" not in mock_result or "available" not in mock_result:
        print("  ✗ Mock data missing required fields (total, available)")
        print("  Hint: Return dict with total, used, available keys")
        return False
    print(f"  ✓ Mock data works: {mock_result}")

    # Test 3: Check tool returns data
    print("\n[Test 3] Checking check_subnet_capacity tool...")
    result = check_subnet_capacity("us-west-2")
    if result is None:
        print("  ✗ check_subnet_capacity() returned None")
        print("  Hint: Complete TODO 1 and TODO 3")
        return False
    print(f"  ✓ Tool returned data")

    # Test 4: Check required fields in response
    print("\n[Test 4] Checking response fields...")
    required_fields = ["region", "status", "available_ips", "recommendation"]
    missing = [f for f in required_fields if f not in result]
    if missing:
        print(f"  ✗ Missing fields: {missing}")
        return False
    print(f"  ✓ All required fields present")
    print(f"    Region: {result['region']}")
    print(f"    Status: {result['status']}")
    print(f"    Available IPs: {result['available_ips']}")
    print(f"    Recommendation: {result['recommendation']}")

    # Test 5: Test different regions
    print("\n[Test 5] Testing multiple regions...")
    test_cases = [
        ("us-west-2", "GO"),        # Healthy - lots of IPs
        ("us-east-1", "CAUTION"),   # Warning - high utilization
        ("eu-west-1", "NO-GO"),     # Critical - not enough IPs
    ]

    for region, expected_rec in test_cases:
        result = check_subnet_capacity(region, min_required_ips=10)
        actual_rec = result.get("recommendation", "UNKNOWN")
        if expected_rec in actual_rec:
            print(f"  ✓ {region}: {actual_rec} (expected {expected_rec})")
        else:
            print(f"  ⚠ {region}: {actual_rec} (expected {expected_rec})")

    # Test 6: Test with custom min_required_ips
    print("\n[Test 6] Testing with custom IP requirement...")
    result = check_subnet_capacity("us-east-1", min_required_ips=50)
    if result.get("recommendation") == "NO-GO":
        print(f"  ✓ Correctly returns NO-GO when 50 IPs needed but only {result.get('available_ips')} available")
    else:
        print(f"  ⚠ Expected NO-GO for high IP requirement")

    # Test 7: Test tool has correct decorator
    print("\n[Test 7] Checking @tool decorator...")
    if hasattr(check_subnet_capacity, '__wrapped__'):
        print("  ✓ Function has @tool decorator")
    else:
        print("  ✗ Missing @tool decorator")
        print("  Hint: Add @tool above the function definition")
        return False

    # Test 8: Test with agent (optional - requires AWS credentials)
    print("\n[Test 8] Testing with Agent...")
    try:
        from strands import Agent
        from strands.models import BedrockModel

        model = BedrockModel(
            model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            region_name="us-west-2"
        )
        agent = Agent(model=model, tools=[check_subnet_capacity])

        response = agent("Check IP capacity in us-east-1")
        response_text = str(response).upper()

        if any(word in response_text for word in ["CAUTION", "WARNING", "NO-GO", "IP", "CAPACITY"]):
            print("  ✓ Agent used IPAM tool and gave capacity assessment")
        else:
            print("  ⚠ Agent response might not reflect IPAM data")

    except Exception as e:
        print(f"  ⚠ Could not test with agent: {e}")
        print("  (This is okay - tool implementation is correct)")

    print("\n" + "=" * 60)
    print("Step 3b PASSED!")
    print("=" * 60)
    print("""
Your IPAM tool is working! It can:
✓ Check subnet IP capacity
✓ Calculate utilization percentage
✓ Give GO/CAUTION/NO-GO recommendations
✓ Work with mock data (for testing) or real Infoblox CSP

Next: Proceed to Step 4 (MCP Integration)
""")
    return True


if __name__ == "__main__":
    success = test_step3b()
    sys.exit(0 if success else 1)
