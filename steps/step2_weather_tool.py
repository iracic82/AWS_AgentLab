"""
Step 2: Agent with Custom Weather Tool
======================================
Now we add our first custom tool - weather forecasting.
The agent can decide to use this tool when asked about weather.

Run: python steps/step2_weather_tool.py
"""

import sys
sys.path.insert(0, "/Users/iracic/PycharmProjects/AWS_AgentLab")

from strands import Agent
from src.config import get_model
from src.tools.weather_tool import get_weather_forecast

# Create agent with our custom tool
agent = Agent(model=get_model(), tools=[get_weather_forecast])

# Test the agent - it should automatically use the weather tool
response = agent("What's the weather like in Seattle right now? Should I be concerned about any datacenter issues?")
print(response)
