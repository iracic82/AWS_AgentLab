"""
Step 6: Package for AWS AgentCore Deployment
============================================
Learn how to package your agent for cloud deployment on AWS AgentCore.

EXERCISE: Create the handler.py entry point that AgentCore uses to run your agent.

Learning objectives:
- Understand AgentCore architecture (serverless microVMs)
- Create the entry point handler with @app.entrypoint decorator
- Package agents for production deployment
- Deploy using agentcore CLI (configure → deploy → invoke)

AgentCore Flow:
1. Your code (handler.py + tools) gets packaged
2. AgentCore configure → generates Dockerfile
3. AgentCore deploy → CodeBuild builds container → ECR stores image → AgentCore runs it
4. Users invoke via agentcore invoke or API

Run: python lab/exercises/step6_agentcore_handler.py (tests locally)
Test: python lab/tests/test_step6.py
Deploy: agentcore configure -e lab/exercises/step6_agentcore_handler.py
"""

# TODO 1: Import BedrockAgentCoreApp from bedrock_agentcore
# This is the main class for AgentCore integration
#
# Hint: from bedrock_agentcore import BedrockAgentCoreApp

from bedrock_agentcore import BedrockAgentCoreApp

from strands import Agent
from strands.models import BedrockModel

# Import your tools (using absolute imports for AgentCore packaging)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from lab.exercises.step2_weather_tool import get_weather_forecast
    from lab.exercises.step3_aws_status_tool import check_aws_status
    from lab.exercises.step3b_ipam_tool import check_subnet_capacity
    from lab.exercises.step5_system_prompt import SYSTEM_PROMPT
except ImportError:
    from lab.solutions.step2_weather_tool import get_weather_forecast
    from lab.solutions.step3_aws_status_tool import check_aws_status
    from lab.solutions.step3b_ipam_tool import check_subnet_capacity
    from lab.solutions.step5_system_prompt import SYSTEM_PROMPT


# TODO 2: Create the AgentCore app instance
# This creates the application that AgentCore will run
#
# Hint: app = BedrockAgentCoreApp()

app = BedrockAgentCoreApp()


# TODO 3: Create the model and agent (same as before)
# We create these at module level so they're ready when requests come in
#
# Hint:
# model = BedrockModel(
#     model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
#     region_name="us-west-2"
# )
#
# agent = Agent(
#     model=model,
#     system_prompt=SYSTEM_PROMPT,
#     tools=[get_weather_forecast, check_aws_status, check_subnet_capacity]
# )

model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-west-2"
)

agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_weather_forecast, check_aws_status, check_subnet_capacity]
)


# TODO 4: Create the entry point function with @app.entrypoint decorator
# This is the function AgentCore calls when it receives a request
#
# The function should:
#   - Take a payload dict as input
#   - Extract the "prompt" from payload (with a default message)
#   - Call the agent with the prompt
#   - Return a dict with the result
#
# Hint:
# @app.entrypoint
# def invoke(payload):
#     """AgentCore invocation entry point."""
#     user_message = payload.get("prompt", "Hello, what can you help me with?")
#     result = agent(user_message)
#     return {"result": result.message}

@app.entrypoint
def invoke(payload):
    """AgentCore invocation entry point."""
    user_message = payload.get("prompt", "Hello, what can you help me with?")
    result = agent(user_message)
    return {"result": result.message}


def test_locally():
    """Test the handler locally before deploying."""
    print("Testing handler locally...")

    if app is None:
        print("ERROR: app not created. Complete TODO 2!")
        return False

    if agent is None:
        print("ERROR: agent not created. Complete TODO 3!")
        return False

    # Check if invoke function exists
    try:
        # Try to find the invoke function
        invoke_fn = None
        for name in dir():
            obj = eval(name)
            if callable(obj) and hasattr(obj, '__wrapped__'):
                invoke_fn = obj
                break

        if invoke_fn is None:
            print("ERROR: invoke function not found. Complete TODO 4!")
            return False

    except Exception as e:
        print(f"ERROR: Could not find invoke function: {e}")
        print("Hint: Make sure you added @app.entrypoint decorator")
        return False

    # Test the agent directly
    print("\nTesting agent...")
    try:
        response = agent("Should I deploy to us-west-2?")
        print(f"Agent response: {str(response)[:200]}...")
        print("\n✓ Handler is ready for AgentCore deployment!")
        return True
    except Exception as e:
        print(f"ERROR: Agent test failed: {e}")
        return False


# This allows AgentCore to run the app
if __name__ == "__main__":
    if test_locally():
        print("\n" + "=" * 60)
        print("Next steps to deploy:")
        print("=" * 60)
        print("""
1. Configure AgentCore:
   agentcore configure -e lab/exercises/step6_agentcore_handler.py \\
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
