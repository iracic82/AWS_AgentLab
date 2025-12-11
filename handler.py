"""
AgentCore Handler
=================
Entry point for deploying the DevOps Decision Agent to AWS AgentCore.

Deploy with:
  agentcore configure -e handler.py
  agentcore deploy
  agentcore invoke '{"prompt": "Should I deploy to us-east-1?"}'

Cleanup with:
  agentcore destroy
"""

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

from src.tools.weather_tool import get_weather_forecast
from src.tools.aws_status_tool import check_aws_status

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# System prompt for the DevOps agent
SYSTEM_PROMPT = """You are a DevOps Decision Assistant. Your job is to help engineers
make informed deployment decisions by analyzing multiple factors:

1. AWS Service Health - Check for any ongoing incidents
2. Weather Conditions - Severe weather can affect datacenters

When asked about deployments:
- Always check relevant AWS regions for health status
- Consider external factors that might impact deployment
- Provide a clear recommendation (GO / NO-GO / CAUTION)
- Explain your reasoning

Be concise but thorough. Engineers need quick, actionable information.
"""

# Create model with explicit config
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-west-2"
)

# Create agent with custom tools
agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_weather_forecast, check_aws_status]
)


@app.entrypoint
def invoke(payload):
    """AgentCore invocation entry point."""
    user_message = payload.get("prompt", "Hello, what can you help me with?")
    result = agent(user_message)
    return {"result": result.message}


if __name__ == "__main__":
    app.run()
