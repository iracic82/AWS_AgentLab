"""
Step 4: Integrate External MCP Server
=====================================
Learn how to connect your agent to external tools via MCP (Model Context Protocol).

EXERCISE: Connect to the Fetch MCP server to give your agent web browsing abilities.

Learning objectives:
- Understand MCP (Model Context Protocol) architecture
- Configure and connect to external MCP servers
- Combine MCP tools with custom tools
- Use context managers for resource management

MCP Info:
- MCP is a standard for connecting AI to external tools
- We'll use the "fetch" MCP server - it can fetch any URL
- This gives our agent access to any web API or page

Prerequisites:
- Python uvx installed (comes with uv)
- mcp-server-fetch package (auto-installed via uvx)

Run: python lab/exercises/step4_mcp_integration.py
Test: python lab/tests/test_step4.py
"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel

# Import your tools from previous steps
try:
    from lab.exercises.step2_weather_tool import get_weather_forecast
    from lab.exercises.step3_aws_status_tool import check_aws_status
except ImportError:
    from lab.solutions.step2_weather_tool import get_weather_forecast
    from lab.solutions.step3_aws_status_tool import check_aws_status


def create_mcp_client():
    """
    Create an MCP client that connects to the Fetch server.
    The Fetch server allows the agent to fetch any URL.
    """

    # TODO 1: Create an MCPClient that connects to mcp-server-fetch
    # The MCPClient takes a lambda that returns a stdio_client
    # The stdio_client needs StdioServerParameters with:
    #   - command: "uvx"
    #   - args: ["mcp-server-fetch"]
    #
    # Hint:
    # mcp_client = MCPClient(lambda: stdio_client(
    #     StdioServerParameters(
    #         command="uvx",
    #         args=["mcp-server-fetch"]
    #     )
    # ))

    mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["mcp-server-fetch"]
        )
    ))

    return mcp_client


def create_agent_with_mcp_and_custom_tools(mcp_client):
    """
    Create an agent that has both MCP tools and custom tools.

    Args:
        mcp_client: An active MCPClient (inside context manager)
    """

    # TODO 2: Get the list of tools from the MCP client
    # Use mcp_client.list_tools_sync() to get available MCP tools
    #
    # Hint: mcp_tools = mcp_client.list_tools_sync()

    mcp_tools = mcp_client.list_tools_sync()

    # TODO 3: Combine custom tools with MCP tools
    # Create a list with your custom tools first, then add MCP tools
    #
    # Hint: all_tools = [get_weather_forecast, check_aws_status] + mcp_tools

    all_tools = [get_weather_forecast, check_aws_status] + mcp_tools

    # TODO 4: Create the agent with all tools
    # Use BedrockModel and pass all_tools to the Agent
    #
    # Hint:
    # model = BedrockModel(
    #     model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    #     region_name="us-west-2"
    # )
    # agent = Agent(model=model, tools=all_tools)

    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )
    agent = Agent(model=model, tools=all_tools)

    return agent


def main():
    """Test MCP integration with custom tools."""
    print("Creating MCP client...")
    mcp_client = create_mcp_client()

    if mcp_client is None:
        print("ERROR: MCP client not created. Complete TODO 1!")
        return

    # TODO 5: Use the MCP client with a context manager
    # The MCP client must be used inside a 'with' statement
    # This ensures proper connection setup and cleanup
    #
    # Structure:
    # with mcp_client:
    #     agent = create_agent_with_mcp_and_custom_tools(mcp_client)
    #     response = agent("your question here")
    #     print(response)

    print("Connecting to MCP server...")

    # Replace this with the context manager pattern from TODO 5
    with mcp_client:
        print("MCP connected! Creating agent...")
        agent = create_agent_with_mcp_and_custom_tools(mcp_client)

        if agent is None:
            print("ERROR: Agent not created. Complete TODOs 2-4!")
            return

        print("\nTesting agent with a question that uses all tool types...")
        response = agent("""
        I want to deploy today. Please:
        1. Check AWS status for us-west-2
        2. Check weather in Oregon
        3. Fetch https://www.githubstatus.com/api/v2/status.json to check GitHub

        Should I deploy?
        """)
        print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
