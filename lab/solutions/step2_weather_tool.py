"""
Step 2: Build Your First Custom Tool - SOLUTION
================================================
"""

import requests
from strands.tools import tool
from strands import Agent
from strands.models import BedrockModel


@tool
def get_weather_forecast(city: str) -> dict:
    """
    Get current weather and forecast for a city.
    Useful for deployment decisions - severe weather can affect datacenters.

    Args:
        city: City name (e.g., "Seattle", "London", "New York")

    Returns:
        Weather data including temperature, conditions, and forecast
    """
    try:
        # Make HTTP request to wttr.in API
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10,
            headers={"User-Agent": "DevOpsAgent/1.0"}
        )

        # Check for errors
        response.raise_for_status()
        data = response.json()

        # Extract current conditions
        current = data.get("current_condition", [{}])[0]

        # Return structured weather data
        return {
            "city": city,
            "temperature_c": current.get("temp_C"),
            "temperature_f": current.get("temp_F"),
            "condition": current.get("weatherDesc", [{}])[0].get("value"),
            "humidity": current.get("humidity"),
            "wind_speed_kmph": current.get("windspeedKmph"),
        }

    except requests.RequestException as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}


def create_agent_with_tool():
    """Create an agent with the weather tool."""
    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    agent = Agent(model=model, tools=[get_weather_forecast])
    return agent


def main():
    """Test the weather tool."""
    print("Testing weather tool directly...")
    result = get_weather_forecast("Seattle")
    print(f"Direct tool call result: {result}")

    print("\nCreating agent with weather tool...")
    agent = create_agent_with_tool()

    print("Testing agent with weather question...")
    response = agent("What's the weather like in Seattle? Is it good for outdoor work?")
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
