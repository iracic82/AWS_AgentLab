"""
Step 1: Hello World Agent - SOLUTION
====================================
"""

from strands import Agent
from strands.models import BedrockModel


def create_agent():
    """Create and return a basic Strands agent."""

    # Create a BedrockModel pointing to Claude on Bedrock
    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    # Create an Agent using the model
    agent = Agent(model=model)

    return agent


def main():
    """Test the agent with a simple question."""
    print("Creating agent...")
    agent = create_agent()
    print("Agent created! Testing...")
    response = agent("What is DevOps in one sentence?")
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
