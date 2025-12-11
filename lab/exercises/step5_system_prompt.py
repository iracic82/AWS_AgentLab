"""
Step 5: Design Your Agent's Personality with System Prompts
===========================================================
Learn how to customize agent behavior using system prompts.

EXERCISE: Write a system prompt that makes your agent a helpful DevOps assistant.

Learning objectives:
- Understand how system prompts shape agent behavior
- Design clear, actionable instructions for agents
- Create agents that give consistent, formatted responses
- Build the complete DevOps Decision Agent

What is a System Prompt?
- Instructions given to the agent BEFORE user messages
- Defines personality, expertise, and response format
- Helps agent give consistent, relevant answers

Run: python lab/exercises/step5_system_prompt.py
Test: python lab/tests/test_step5.py
Solution: lab/solutions/step5_system_prompt.py
"""

from strands import Agent
from strands.models import BedrockModel

# Import your tools from previous steps (use solutions as fallback)
try:
    from lab.solutions.step2_weather_tool import get_weather_forecast
    from lab.solutions.step3_aws_status_tool import check_aws_status
    from lab.solutions.step3b_ipam_tool import check_subnet_capacity
except ImportError:
    get_weather_forecast = None
    check_aws_status = None
    check_subnet_capacity = None


# TODO 1: Write a system prompt for your DevOps Decision Agent
# The system prompt should:
#   - Define the agent's role (DevOps Decision Assistant)
#   - List what factors it should check (AWS health, weather, IP capacity)
#   - Specify response format (GO / NO-GO / CAUTION recommendation)
#   - Tell it to be concise but thorough
#
# Example structure:
# """You are a [role]. Your job is to [task].
#
# When asked about deployments:
# - Check [factor 1]
# - Check [factor 2]
# - Check [factor 3]
# - Provide a clear recommendation: GO / NO-GO / CAUTION
# - Explain your reasoning
#
# Be [tone] and [style].
# """
#
# Hint - a good system prompt includes:
# 1. Role definition: "You are a DevOps Decision Assistant..."
# 2. Task description: "Your job is to help engineers make deployment decisions..."
# 3. Tool usage instructions: "Use check_aws_status, get_weather_forecast, check_subnet_capacity..."
# 4. Response format: "Provide a clear GO / NO-GO / CAUTION recommendation..."
# 5. Style guidance: "Be concise but thorough..."

SYSTEM_PROMPT = """
TODO: Write your system prompt here!

Replace this placeholder with your DevOps Decision Agent system prompt.
See the hints above for guidance.
"""


def create_devops_agent():
    """Create the complete DevOps Decision Agent with system prompt."""

    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    # TODO 2: Create an agent with:
    #   - The model
    #   - The system_prompt (use SYSTEM_PROMPT variable)
    #   - All three tools: [get_weather_forecast, check_aws_status, check_subnet_capacity]
    #
    # Hint:
    # agent = Agent(
    #     model=model,
    #     system_prompt=SYSTEM_PROMPT,
    #     tools=[get_weather_forecast, check_aws_status, check_subnet_capacity]
    # )

    agent = None  # Replace with your code

    return agent


def run_interactive():
    """Run the agent in interactive mode."""
    print("=" * 60)
    print("DevOps Decision Agent")
    print("=" * 60)
    print("Ask me about deployments!")
    print("Type 'quit' to exit.\n")

    agent = create_devops_agent()

    if agent is None:
        print("ERROR: Agent not created. Complete the TODOs!")
        return

    # TODO 3: Implement the interactive loop
    # Structure:
    # while True:
    #     user_input = input("You: ").strip()
    #     if user_input.lower() in ["quit", "exit", "q"]:
    #         print("Goodbye!")
    #         break
    #     if not user_input:
    #         continue
    #     response = agent(user_input)
    #     print(f"\nAgent: {response}\n")

    print("TODO 3: Implement the interactive loop")
    print("Hint: Check lab/solutions/step5_system_prompt.py if stuck")


def main():
    """Test the DevOps agent."""
    print("Creating DevOps Decision Agent...")

    # Check if system prompt was written
    if "TODO" in SYSTEM_PROMPT or not SYSTEM_PROMPT.strip():
        print("ERROR: System prompt not written. Complete TODO 1!")
        print("Hint: Check lab/solutions/step5_system_prompt.py for example")
        return

    agent = create_devops_agent()

    if agent is None:
        print("ERROR: Agent not created. Complete TODO 2!")
        return

    print(f"System prompt length: {len(SYSTEM_PROMPT)} characters")
    print("\nTesting agent with deployment question...")

    response = agent("Should I deploy to us-west-2 right now?")
    print(f"\nAgent response:\n{response}")

    # Check if response contains expected elements
    response_text = str(response).upper()
    has_recommendation = any(word in response_text for word in ["GO", "CAUTION", "NO-GO", "PROCEED", "SAFE"])

    if has_recommendation:
        print("\n✓ Agent gave a clear recommendation!")
    else:
        print("\n⚠ Agent didn't give a clear GO/NO-GO recommendation.")
        print("  Hint: Improve your system prompt to request clear recommendations")


if __name__ == "__main__":
    main()
