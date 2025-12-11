"""
Step 1: Hello World Agent
=========================
The simplest possible Strands agent - just a few lines of code.
This verifies your AWS credentials and Bedrock access work.

Prerequisites:
- AWS credentials configured (aws configure)
- Bedrock model access enabled for Claude in us-west-2

Run: python steps/step1_hello_agent.py
"""

from strands import Agent
from strands.models import BedrockModel

# Create Bedrock model with cross-region inference profile
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-west-2"
)

# Create agent with the model
agent = Agent(model=model)

# Test the agent
response = agent("Hello! What can you help me with as a DevOps assistant?")
print(response)
