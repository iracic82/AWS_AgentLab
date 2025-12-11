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
"""

from strands import Agent
from strands.models import BedrockModel

# Import your tools from previous steps
try:
    from lab.exercises.step2_weather_tool import get_weather_forecast
    from lab.exercises.step3_aws_status_tool import check_aws_status
    from lab.exercises.step3b_ipam_tool import check_subnet_capacity
except ImportError:
    from lab.solutions.step2_weather_tool import get_weather_forecast
    from lab.solutions.step3_aws_status_tool import check_aws_status
    from lab.solutions.step3b_ipam_tool import check_subnet_capacity


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
# - Provide a clear recommendation: GO / NO-GO / CAUTION
# - Explain your reasoning
#
# Be [tone] and [style].
# """

SYSTEM_PROMPT = """You are a DevOps Decision Assistant. Your job is to help engineers
make informed deployment decisions by analyzing multiple factors.

When asked about deployments, you should:
1. Check AWS Service Health - Use the check_aws_status tool to verify no ongoing incidents
2. Check Weather Conditions - Use get_weather_forecast for the datacenter region (severe weather can affect infrastructure)
3. Check IP Capacity - Use check_subnet_capacity to verify enough IP addresses are available for new instances

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

    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_weather_forecast, check_aws_status, check_subnet_capacity]
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


def main():
    """Test the DevOps agent."""
    print("Creating DevOps Decision Agent...")

    agent = create_devops_agent()

    if agent is None:
        print("ERROR: Agent not created. Complete TODO 2!")
        return

    if not SYSTEM_PROMPT.strip() or "TODO" in SYSTEM_PROMPT:
        print("ERROR: System prompt not written. Complete TODO 1!")
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
