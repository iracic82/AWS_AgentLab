"""
DevOps Decision Agent
=====================
A complete agent that helps with deployment decisions by checking:
- AWS service health
- Weather conditions (datacenter regions)
- External service status (via MCP)

This is the main agent file used for local testing and AgentCore deployment.
"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

from config import get_model
from tools.weather_tool import get_weather_forecast
from tools.aws_status_tool import check_aws_status


# System prompt that defines the agent's personality and behavior
SYSTEM_PROMPT = """You are a DevOps Decision Assistant. Your job is to help engineers
make informed deployment decisions by analyzing multiple factors:

1. AWS Service Health - Check for any ongoing incidents
2. Weather Conditions - Severe weather can affect datacenters
3. External Dependencies - Check status of GitHub, CI/CD pipelines, etc.

When asked about deployments:
- Always check relevant AWS regions for health status
- Consider external factors that might impact deployment
- Provide a clear recommendation (GO / NO-GO / CAUTION)
- Explain your reasoning

Be concise but thorough. Engineers need quick, actionable information.
"""


def create_agent_simple() -> Agent:
    """Create agent without MCP (simpler, no context manager needed)."""
    return Agent(
        model=get_model(),
        system_prompt=SYSTEM_PROMPT,
        tools=[get_weather_forecast, check_aws_status]
    )


def run_interactive():
    """Run the agent in interactive mode."""
    print("=" * 60)
    print("DevOps Decision Agent")
    print("=" * 60)
    print("Ask me about deployments, AWS status, or weather conditions.")
    print("Type 'quit' to exit.\n")

    # Try to use MCP, fall back to simple if not available
    try:
        fetch_mcp = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="uvx",
                args=["mcp-server-fetch"]
            )
        ))

        with fetch_mcp:
            mcp_tools = fetch_mcp.list_tools_sync()
            all_tools = [get_weather_forecast, check_aws_status] + mcp_tools

            agent = Agent(
                model=get_model(),
                system_prompt=SYSTEM_PROMPT,
                tools=all_tools
            )

            print("[MCP Fetch server connected]\n")
            _interactive_loop(agent)

    except Exception as e:
        print(f"[MCP not available: {e}]")
        print("[Running with custom tools only]\n")

        agent = create_agent_simple()
        _interactive_loop(agent)


def _interactive_loop(agent: Agent):
    """Run the interactive conversation loop."""
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            if not user_input:
                continue

            response = agent(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    run_interactive()
