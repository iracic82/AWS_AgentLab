"""
Step 4: Agent with MCP Integration
==================================
Add external MCP server (Fetch) for web fetching capabilities.
This shows how Strands integrates with the MCP ecosystem.

Prerequisites:
- Node.js installed (for npx)

Run: python steps/step4_mcp_integration.py
"""

import sys
sys.path.insert(0, "/Users/iracic/PycharmProjects/AWS_AgentLab")

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from src.config import get_model
from src.tools.weather_tool import get_weather_forecast
from src.tools.aws_status_tool import check_aws_status


def main():
    # Create MCP client for Fetch server
    # This gives our agent the ability to fetch any URL
    # Using uvx to run the Python-based fetch MCP server
    fetch_mcp = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["mcp-server-fetch"]
        )
    ))

    # Use context manager to ensure proper connection lifecycle
    with fetch_mcp:
        # Get MCP tools
        mcp_tools = fetch_mcp.list_tools_sync()

        # Combine custom tools with MCP tools
        all_tools = [get_weather_forecast, check_aws_status] + mcp_tools

        # Create agent with all tools
        agent = Agent(model=get_model(), tools=all_tools)

        # Test the agent - now it can fetch web pages too!
        response = agent("""
        I want to deploy to AWS today. Please:
        1. Check the AWS status for us-east-1
        2. Check the weather in Virginia
        3. Fetch https://www.githubstatus.com/api/v2/status.json to see if GitHub is up

        Based on all this info, should I deploy?
        """)
        print(response)


if __name__ == "__main__":
    main()
