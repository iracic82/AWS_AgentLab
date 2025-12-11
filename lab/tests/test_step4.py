"""
Test Step 4: Verify MCP Integration
===================================
Run: python lab/tests/test_step4.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step4():
    """Test that Step 4 is correctly implemented."""
    print("=" * 60)
    print("Testing Step 4: MCP Integration")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step4_mcp_integration import create_mcp_client, create_agent_with_mcp_and_custom_tools
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check MCP client creation
    print("\n[Test 2] Checking MCP client creation...")
    try:
        mcp_client = create_mcp_client()
        if mcp_client is None:
            print("  ✗ MCP client is None")
            print("  Hint: Complete TODO 1 - create MCPClient with stdio_client")
            return False
        print("  ✓ MCP client created")
    except Exception as e:
        print(f"  ✗ MCP client creation failed: {e}")
        return False

    # Test 3: Check MCP connection works
    print("\n[Test 3] Testing MCP connection...")
    try:
        with mcp_client:
            print("  ✓ MCP connection established")

            # Test 4: Check tools are retrieved
            print("\n[Test 4] Checking MCP tools retrieval...")
            mcp_tools = mcp_client.list_tools_sync()
            if not mcp_tools:
                print("  ✗ No MCP tools retrieved")
                print("  Hint: Make sure mcp-server-fetch is working")
                return False
            print(f"  ✓ Retrieved {len(mcp_tools)} MCP tools")

            # Test 5: Check agent creation with all tools
            print("\n[Test 5] Checking agent with all tools...")
            agent = create_agent_with_mcp_and_custom_tools(mcp_client)
            if agent is None:
                print("  ✗ Agent is None")
                print("  Hint: Complete TODOs 2-4")
                return False

            print(f"  ✓ Agent created with tools")

            # Test 6: Agent can use MCP tool
            print("\n[Test 6] Testing agent uses MCP fetch tool...")
            try:
                response = agent("Fetch https://httpbin.org/get and tell me the origin IP")
                print(f"  ✓ Agent used MCP fetch tool successfully")
            except Exception as e:
                print(f"  ✗ Agent MCP tool usage failed: {e}")
                return False

    except Exception as e:
        print(f"  ✗ MCP test failed: {e}")
        print("  Hint: Make sure uvx and mcp-server-fetch are available")
        return False

    print("\n" + "=" * 60)
    print("Step 4 PASSED! You can proceed to Step 5.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_step4()
    sys.exit(0 if success else 1)
