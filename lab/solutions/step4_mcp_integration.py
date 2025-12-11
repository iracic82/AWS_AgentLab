"""
Step 4: Integrate External MCP Server - SOLUTION
================================================
"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel

# Import tools from previous steps
try:
    from lab.solutions.step2_weather_tool import get_weather_forecast
    from lab.solutions.step3_aws_status_tool import check_aws_status
except ImportError:
    from lab.exercises.step2_weather_tool import get_weather_forecast
    from lab.exercises.step3_aws_status_tool import check_aws_status


def create_mcp_client():
    """Create an MCP client that connects to the Fetch server."""
    mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["mcp-server-fetch"]
        )
    ))
    return mcp_client


def create_agent_with_mcp_and_custom_tools(mcp_client):
    """Create an agent that has both MCP tools and custom tools."""

    # Get MCP tools
    mcp_tools = mcp_client.list_tools_sync()

    # Combine custom tools with MCP tools
    all_tools = [get_weather_forecast, check_aws_status] + mcp_tools

    # Create the agent
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

    print("Connecting to MCP server...")

    # Use context manager for proper connection handling
    with mcp_client:
        print("MCP connected! Creating agent...")
        agent = create_agent_with_mcp_and_custom_tools(mcp_client)

        print(f"Agent has {len(agent.tools)} tools available")

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
