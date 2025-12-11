"""
Step 5: Design Your Agent's Personality - SOLUTION
==================================================
"""

from strands import Agent
from strands.models import BedrockModel

# Import tools from previous steps
try:
    from lab.solutions.step2_weather_tool import get_weather_forecast
    from lab.solutions.step3_aws_status_tool import check_aws_status
except ImportError:
    from lab.exercises.step2_weather_tool import get_weather_forecast
    from lab.exercises.step3_aws_status_tool import check_aws_status


SYSTEM_PROMPT = """You are a DevOps Decision Assistant. Your job is to help engineers
make informed deployment decisions by analyzing multiple factors.

When asked about deployments, you should:
1. Check AWS Service Health - Use the check_aws_status tool to verify no ongoing incidents
2. Check Weather Conditions - Use get_weather_forecast for the datacenter region (severe weather can affect infrastructure)

After gathering information, provide a clear recommendation:
- GO: All systems healthy, proceed with deployment
- CAUTION: Minor concerns, proceed with extra monitoring
- NO-GO: Significant issues detected, delay deployment

Always explain your reasoning based on the data you collected.

Be concise but thorough. Engineers need quick, actionable information.
Format your final recommendation prominently so it's easy to spot.
"""


def create_devops_agent():
    """Create the complete DevOps Decision Agent with system prompt."""

    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_weather_forecast, check_aws_status]
    )

    return agent


def run_interactive():
    """Run the agent in interactive mode."""
    print("=" * 60)
    print("DevOps Decision Agent")
    print("=" * 60)
    print("Ask me about deployments!")
    print("Type 'quit' to exit.\n")

    agent = create_devops_agent()

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


def main():
    """Test the DevOps agent."""
    print("Creating DevOps Decision Agent...")
    agent = create_devops_agent()

    print(f"System prompt length: {len(SYSTEM_PROMPT)} characters")
    print("\nTesting agent with deployment question...")

    response = agent("Should I deploy to us-west-2 right now?")
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
