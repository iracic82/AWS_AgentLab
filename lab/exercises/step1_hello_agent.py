"""
Step 1: Hello World Agent
=========================
Verify your setup works by creating the simplest possible agent.

EXERCISE: Complete the code below to create a basic Strands agent.

Learning objectives:
- Understand how to import Strands components
- Configure a Bedrock model
- Create and invoke an agent

Run: python lab/exercises/step1_hello_agent.py
Test: python lab/tests/test_step1.py
"""

# TODO 1: Import the Agent class from strands
# Hint: from strands import Agent
from strands import Agent

# TODO 2: Import BedrockModel from strands.models
# Hint: from strands.models import BedrockModel
from strands.models import BedrockModel


def create_agent():
    """Create and return a basic Strands agent."""

    # TODO 3: Create a BedrockModel with these settings:
    #   - model_id: "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    #   - region_name: "us-west-2"
    # Hint: model = BedrockModel(model_id="...", region_name="...")

    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    # TODO 4: Create an Agent using the model
    # Hint: agent = Agent(model=model)

    agent = Agent(model=model)

    return agent


def main():
    """Test the agent with a simple question."""
    print("Creating agent...")
    agent = create_agent()

    if agent is None:
        print("ERROR: Agent not created. Complete the TODOs first!")
        return

    print("Agent created! Testing...")
    response = agent("What is DevOps in one sentence?")
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
