"""
Step 3: Agent with AWS Status Tool
==================================
Add AWS health status checking capability.
Now our agent can check if AWS is having issues before recommending deployment.

Run: python steps/step3_aws_status_tool.py
"""

import sys
sys.path.insert(0, "/Users/iracic/PycharmProjects/AWS_AgentLab")

from strands import Agent
from src.config import get_model
from src.tools.weather_tool import get_weather_forecast
from src.tools.aws_status_tool import check_aws_status

# Create agent with both custom tools
agent = Agent(model=get_model(), tools=[get_weather_forecast, check_aws_status])

# Test the agent with a deployment question
response = agent("""
I'm planning to deploy my application to us-east-1.
Can you check if AWS is having any issues in that region?
Also, what's the weather like in Virginia (where us-east-1 is located)?
""")
print(response)
