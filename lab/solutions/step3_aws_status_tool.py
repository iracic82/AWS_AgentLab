"""
Step 3: Build AWS Status Checker Tool - SOLUTION
================================================
"""

import requests
from strands.tools import tool
from strands import Agent
from strands.models import BedrockModel

# Import weather tool from Step 2
try:
    from lab.solutions.step2_weather_tool import get_weather_forecast
except ImportError:
    from lab.exercises.step2_weather_tool import get_weather_forecast


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
    try:
        # Make HTTP request to AWS status RSS feed
        response = requests.get(
            "https://status.aws.amazon.com/rss/all.rss",
            timeout=10,
            headers={"User-Agent": "DevOpsAgent/1.0"}
        )

        # Check for errors
        response.raise_for_status()

        # Check if region is mentioned in the feed
        content = response.text.lower()
        region_mentioned = region.lower() in content

        # Return status based on findings
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

    except requests.RequestException as e:
        return {
            "region": region,
            "status": "unknown",
            "message": f"Could not fetch AWS status. Check manually.",
            "error": str(e)
        }


def create_agent_with_both_tools():
    """Create an agent with BOTH weather and AWS status tools."""
    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    agent = Agent(model=model, tools=[get_weather_forecast, check_aws_status])
    return agent


def main():
    """Test the AWS status tool."""
    print("Testing AWS status tool directly...")
    result = check_aws_status("us-west-2")
    print(f"Direct tool call result: {result}")

    print("\nCreating agent with BOTH tools...")
    agent = create_agent_with_both_tools()

    print("\nTesting agent with deployment question...")
    response = agent("""
    I want to deploy to us-west-2 (Oregon).
    Can you check AWS status and weather conditions?
    Should I proceed with the deployment?
    """)
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
