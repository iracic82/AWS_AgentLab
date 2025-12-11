"""
Step 6: Package for AWS AgentCore Deployment - SOLUTION
=======================================================
"""

# Import BedrockAgentCoreApp from bedrock_agentcore
from bedrock_agentcore import BedrockAgentCoreApp

from strands import Agent
from strands.models import BedrockModel

# Import tools (using absolute imports for AgentCore packaging)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from lab.solutions.step2_weather_tool import get_weather_forecast
    from lab.solutions.step3_aws_status_tool import check_aws_status
    from lab.solutions.step5_system_prompt import SYSTEM_PROMPT
except ImportError:
    from lab.exercises.step2_weather_tool import get_weather_forecast
    from lab.exercises.step3_aws_status_tool import check_aws_status
    from lab.exercises.step5_system_prompt import SYSTEM_PROMPT


# Create the AgentCore app instance
app = BedrockAgentCoreApp()


# Create the model and agent at module level
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-west-2"
)

agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_weather_forecast, check_aws_status]
)


# Entry point function with @app.entrypoint decorator
@app.entrypoint
def invoke(payload):
    """AgentCore invocation entry point.

    This function is called by AgentCore when it receives a request.

    Args:
        payload: Dict containing the request data, typically {"prompt": "user message"}

    Returns:
        Dict with the agent's response
    """
    user_message = payload.get("prompt", "Hello, what can you help me with?")
    result = agent(user_message)
    return {"result": result.message}


def test_locally():
    """Test the handler locally before deploying."""
    print("Testing handler locally...")

    print("\n[Check 1] App instance...")
    if app is None:
        print("  ERROR: app not created")
        return False
    print("  ✓ App created")

    print("\n[Check 2] Agent instance...")
    if agent is None:
        print("  ERROR: agent not created")
        return False
    print("  ✓ Agent created")

    print("\n[Check 3] Entry point function...")
    if not hasattr(invoke, '__wrapped__'):
        print("  ERROR: invoke function not decorated with @app.entrypoint")
        return False
    print("  ✓ Entry point configured")

    print("\n[Check 4] Testing agent invocation...")
    try:
        response = agent("Should I deploy to us-west-2?")
        print(f"  Agent response: {str(response)[:200]}...")
        print("  ✓ Agent working")
    except Exception as e:
        print(f"  ERROR: Agent test failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("Handler is ready for AgentCore deployment!")
    print("=" * 60)
    return True


# This allows AgentCore to run the app
if __name__ == "__main__":
    if test_locally():
        print("""
Next steps to deploy:
=====================

1. Configure AgentCore:
   agentcore configure -e lab/solutions/step6_agentcore_handler.py \\
       -r us-west-2 --disable-memory -n devops_agent

2. Deploy to AgentCore:
   agentcore deploy

3. Test the deployed agent:
   agentcore invoke '{"prompt": "Should I deploy to us-east-1?"}'

4. Check status:
   agentcore status

5. Clean up when done:
   agentcore destroy
""")
