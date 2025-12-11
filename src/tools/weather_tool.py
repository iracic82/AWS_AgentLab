"""
Custom Tool: Weather Forecast
=============================
Uses the free wttr.in API - no API key required!
"""

import requests
from strands.tools import tool


@tool
def get_weather_forecast(city: str) -> dict:
    """
    Get current weather and forecast for a city.
    Useful for deployment decisions - severe weather can affect datacenters.

    Args:
        city: City name (e.g., "London", "New York", "us-east-1")

    Returns:
        Weather data including temperature, conditions, and forecast
    """
    try:
        # wttr.in is a free weather API - no key needed
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10,
            headers={"User-Agent": "DevOpsAgent/1.0"}
        )
        response.raise_for_status()
        data = response.json()

        # Extract relevant info
        current = data.get("current_condition", [{}])[0]

        return {
            "city": city,
            "temperature_c": current.get("temp_C"),
            "temperature_f": current.get("temp_F"),
            "condition": current.get("weatherDesc", [{}])[0].get("value"),
            "humidity": current.get("humidity"),
            "wind_speed_kmph": current.get("windspeedKmph"),
            "visibility_km": current.get("visibility"),
            "uv_index": current.get("uvIndex"),
        }
    except requests.RequestException as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}
    except (KeyError, IndexError) as e:
        return {"error": f"Failed to parse weather data: {str(e)}"}
