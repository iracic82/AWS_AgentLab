"""
Step 3: Build AWS Status Checker Tool
=====================================
Build a tool that checks AWS service health before deployments.

EXERCISE: Implement an AWS status checker using the public RSS feed.

Learning objectives:
- Work with RSS/XML data from web APIs
- Parse responses and extract relevant information
- Build tools that inform deployment decisions
- Combine multiple tools in one agent

API Info:
- AWS publishes status at: https://status.aws.amazon.com/rss/all.rss
- It's an RSS feed (XML) with recent service events
- We'll check if a region is mentioned in recent issues

Run: python lab/exercises/step3_aws_status_tool.py
Test: python lab/tests/test_step3.py
"""

import requests
from strands.tools import tool
from strands import Agent
from strands.models import BedrockModel

# Import your weather tool from Step 2
# We'll combine both tools in one agent!
try:
    from lab.exercises.step2_weather_tool import get_weather_forecast
except ImportError:
    # Fallback if step2 not completed
    from lab.solutions.step2_weather_tool import get_weather_forecast


# TODO 1: Add the @tool decorator
@tool
def check_aws_status(region: str = "us-east-1") -> dict:
    """
    Check AWS service health status for a specific region.
    Useful before deployments to ensure AWS services are healthy.

    Args:
        region: AWS region to check (e.g., "us-east-1", "us-west-2", "eu-west-1")

    Returns:
        Current AWS service status and any ongoing incidents
    """

    # TODO 2: Make an HTTP GET request to the AWS status RSS feed
    # URL: "https://status.aws.amazon.com/rss/all.rss"
    # Use requests.get() with timeout=10 and a User-Agent header
    #
    # Hint:
    # response = requests.get(
    #     "https://status.aws.amazon.com/rss/all.rss",
    #     timeout=10,
    #     headers={"User-Agent": "DevOpsAgent/1.0"}
    # )

    response = requests.get(
        "https://status.aws.amazon.com/rss/all.rss",
        timeout=10,
        headers={"User-Agent": "DevOpsAgent/1.0"}
    )

    # TODO 3: Check if the request was successful
    # Use response.raise_for_status()

    response.raise_for_status()

    # TODO 4: Check if the region is mentioned in the RSS feed content
    # Convert response.text to lowercase and check if region.lower() is in it
    #
    # Hint:
    # content = response.text.lower()
    # region_mentioned = region.lower() in content

    content = response.text.lower()
    region_mentioned = region.lower() in content

    # TODO 5: Return appropriate status based on whether region is mentioned
    # If region is mentioned in the feed, there might be issues
    # If not mentioned, the region is likely healthy
    #
    # Hint:
    # if region_mentioned:
    #     return {
    #         "region": region,
    #         "status": "check_needed",
    #         "message": f"AWS status feed mentions {region}. Check health dashboard.",
    #         "recommendation": "Review AWS Health Dashboard before deploying"
    #     }
    # else:
    #     return {
    #         "region": region,
    #         "status": "healthy",
    #         "message": f"No recent issues found for {region}.",
    #         "recommendation": "Safe to proceed with deployment"
    #     }

    if region_mentioned:
        return {
            "region": region,
            "status": "check_needed",
            "message": f"AWS status feed mentions {region}. Check health dashboard.",
            "recommendation": "Review AWS Health Dashboard before deploying"
        }
    else:
        return {
            "region": region,
            "status": "healthy",
            "message": f"No recent issues found for {region}.",
            "recommendation": "Safe to proceed with deployment"
        }


def create_agent_with_both_tools():
    """Create an agent with BOTH weather and AWS status tools."""
    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    # TODO 6: Create an agent with BOTH tools
    # Pass tools=[get_weather_forecast, check_aws_status] to the Agent
    #
    # Hint: agent = Agent(model=model, tools=[get_weather_forecast, check_aws_status])

    agent = Agent(model=model, tools=[get_weather_forecast, check_aws_status])

    return agent


def main():
    """Test the AWS status tool."""
    print("Testing AWS status tool directly...")

    result = check_aws_status("us-west-2")
    print(f"Direct tool call result: {result}")

    if not result.get("status"):
        print("\nERROR: Tool not returning data. Complete the TODOs!")
        return

    print("\nCreating agent with BOTH tools...")
    agent = create_agent_with_both_tools()

    if agent is None:
        print("ERROR: Agent not created. Complete TODO 6!")
        return

    print("\nTesting agent with deployment question...")
    response = agent("""
    I want to deploy to us-west-2 (Oregon).
    Can you check AWS status and weather conditions?
    Should I proceed with the deployment?
    """)
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
