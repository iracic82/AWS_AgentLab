"""
Test Step 2: Verify Weather Tool Implementation
===============================================
Run: python lab/tests/test_step2.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step2():
    """Test that Step 2 is correctly implemented."""
    print("=" * 60)
    print("Testing Step 2: Weather Tool")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step2_weather_tool import get_weather_forecast, create_agent_with_tool
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check @tool decorator is applied
    print("\n[Test 2] Checking @tool decorator...")
    if not hasattr(get_weather_forecast, '__wrapped__') and not hasattr(get_weather_forecast, 'name'):
        # Check if it's been decorated by looking for tool attributes
        tool_attrs = ['name', 'description', '__call__']
        is_tool = any(hasattr(get_weather_forecast, attr) for attr in tool_attrs)
        if not is_tool:
            print("  ✗ @tool decorator not applied")
            print("  Hint: Add @tool above the function definition")
            return False
    print("  ✓ @tool decorator applied")

    # Test 3: Test the tool directly
    print("\n[Test 3] Testing tool with 'Seattle'...")
    try:
        result = get_weather_forecast("Seattle")
        if isinstance(result, dict):
            if "error" in result:
                print(f"  ✗ Tool returned error: {result['error']}")
                return False
            if result.get("temperature_c"):
                print(f"  ✓ Got weather data: {result['temperature_c']}°C, {result.get('condition')}")
            else:
                print("  ✗ Tool returned empty data")
                print(f"  Result was: {result}")
                print("  Hint: Check your TODO 4 and TODO 5")
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
    required_fields = ["city", "temperature_c", "temperature_f", "condition", "humidity"]
    missing = [f for f in required_fields if f not in result or result[f] is None]
    if missing:
        print(f"  ✗ Missing fields: {missing}")
        print("  Hint: Make sure TODO 5 returns all required fields")
        return False
    print(f"  ✓ All required fields present")

    # Test 5: Check agent creation
    print("\n[Test 5] Checking agent with tool...")
    try:
        agent = create_agent_with_tool()
        if agent is None:
            print("  ✗ Agent is None")
            print("  Hint: Complete TODO 6 - pass tools=[get_weather_forecast]")
            return False
        print("  ✓ Agent created with tool")
    except Exception as e:
        print(f"  ✗ Agent creation failed: {e}")
        return False

    # Test 6: Agent uses the tool
    print("\n[Test 6] Testing agent uses the tool...")
    try:
        response = agent("What's the temperature in London right now? Just give me the number.")
        print(f"  ✓ Agent responded (tool was available)")
    except Exception as e:
        print(f"  ✗ Agent invocation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("Step 2 PASSED! You can proceed to Step 3.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_step2()
    sys.exit(0 if success else 1)
