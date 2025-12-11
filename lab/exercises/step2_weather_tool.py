"""
Step 2: Build Your First Custom Tool - Weather Forecast
========================================================
Learn how to create custom tools that your agent can use.

EXERCISE: Implement a weather forecast tool using the @tool decorator.

Learning objectives:
- Understand the @tool decorator
- Make HTTP requests to external APIs
- Return structured data from tools
- Handle errors gracefully

API Info:
- We'll use wttr.in - a free weather API (no API key needed!)
- URL format: https://wttr.in/{city}?format=j1
- Returns JSON with weather data

Run: python lab/exercises/step2_weather_tool.py
Test: python lab/tests/test_step2.py
Solution: lab/solutions/step2_weather_tool.py
"""

import requests
from strands.tools import tool
from strands import Agent
from strands.models import BedrockModel


# TODO 1: Add the @tool decorator above this function
# Hint: Just add @tool on the line before 'def get_weather_forecast'

def get_weather_forecast(city: str) -> dict:
    """
    Get current weather and forecast for a city.
    Useful for deployment decisions - severe weather can affect datacenters.

    Args:
        city: City name (e.g., "Seattle", "London", "New York")

    Returns:
        Weather data including temperature, conditions, and forecast
    """

    # TODO 2: Make an HTTP GET request to the wttr.in API
    # URL: f"https://wttr.in/{city}?format=j1"
    # Use requests.get() with timeout=10 and a User-Agent header
    #
    # Hint:
    # response = requests.get(
    #     f"https://wttr.in/{city}?format=j1",
    #     timeout=10,
    #     headers={"User-Agent": "DevOpsAgent/1.0"}
    # )

    response = None  # Replace with your code

    # TODO 3: Check if the request was successful and parse JSON
    # Use response.raise_for_status() to check for errors
    # Then parse JSON with response.json()
    #
    # Hint:
    # response.raise_for_status()
    # data = response.json()

    data = None  # Replace with your code

    # TODO 4: Extract the current conditions from the response
    # The API returns data in this structure:
    #   data["current_condition"][0]["temp_C"]  -> temperature in Celsius
    #   data["current_condition"][0]["temp_F"]  -> temperature in Fahrenheit
    #   data["current_condition"][0]["weatherDesc"][0]["value"]  -> description
    #   data["current_condition"][0]["humidity"]  -> humidity percentage
    #   data["current_condition"][0]["windspeedKmph"]  -> wind speed
    #
    # Hint:
    # current = data.get("current_condition", [{}])[0]

    current = None  # Replace with your code

    # TODO 5: Return a dictionary with the extracted weather data
    # Include: city, temperature_c, temperature_f, condition, humidity, wind_speed_kmph
    #
    # Hint:
    # return {
    #     "city": city,
    #     "temperature_c": current.get("temp_C"),
    #     "temperature_f": current.get("temp_F"),
    #     "condition": current.get("weatherDesc", [{}])[0].get("value"),
    #     "humidity": current.get("humidity"),
    #     "wind_speed_kmph": current.get("windspeedKmph"),
    # }

    return {}  # Replace with your code


def create_agent_with_tool():
    """Create an agent with the weather tool."""
    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    # TODO 6: Create an agent with the weather tool
    # Pass tools=[get_weather_forecast] to the Agent constructor
    #
    # Hint: agent = Agent(model=model, tools=[get_weather_forecast])

    agent = None  # Replace with your code

    return agent


def main():
    """Test the weather tool."""
    print("Testing weather tool directly...")

    # Test the tool function directly first
    result = get_weather_forecast("Seattle")
    print(f"Direct tool call result: {result}")

    if not result.get("temperature_c"):
        print("\nERROR: Tool not returning data. Complete the TODOs!")
        print("Hint: Check lab/solutions/step2_weather_tool.py if stuck")
        return

    print("\nCreating agent with weather tool...")
    agent = create_agent_with_tool()

    if agent is None:
        print("ERROR: Agent not created. Complete TODO 6!")
        return

    print("Testing agent with weather question...")
    response = agent("What's the weather like in Seattle? Is it good for outdoor work?")
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
