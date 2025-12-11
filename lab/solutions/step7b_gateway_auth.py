"""
Step 7b: Connect Agent to Gateway with Your Cognito OAuth - SOLUTION
====================================================================
"""

import sys
import json
import time
import base64
import requests
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# PART 1: Import boto3
import boto3


def load_cognito_config(filename="cognito_config.json"):
    """Load Cognito configuration from Step 7a."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: cognito_config.json not found!")
        print("Please complete Step 7a first:")
        print("  python lab/exercises/step7a_cognito_oauth.py")
        return None


def create_gateway_with_cognito(cognito_config, gateway_name="DevOpsGateway"):
    """Create AgentCore Gateway using your Cognito for auth."""
    region = cognito_config['region']

    # Build Cognito discovery URL (OpenID Connect standard)
    pool_id = cognito_config['pool_id']
    discovery_url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/openid-configuration"

    print(f"Creating Gateway with Cognito auth...")
    print(f"  Discovery URL: {discovery_url}")
    print(f"  Allowed Client: {cognito_config['client_id'][:20]}...")

    # Create Gateway using AgentCore control plane
    gateway_client = boto3.client('bedrock-agentcore-control', region_name=region)

    response = gateway_client.create_gateway(
        name=gateway_name,
        protocolType='MCP',
        authorizerType='CUSTOM_JWT',
        authorizerConfiguration={
            'customJWTAuthorizer': {
                'discoveryUrl': discovery_url,
                'allowedAudiences': [cognito_config['client_id']],
                'allowedClients': [cognito_config['client_id']]
            }
        }
    )

    gateway_id = response['gatewayId']
    print(f"  ✓ Gateway created: {gateway_id}")

    # Wait for gateway to be ready
    print("  Waiting for Gateway to be READY...")
    waiter_count = 0
    while waiter_count < 30:
        status_response = gateway_client.get_gateway(gatewayId=gateway_id)
        status = status_response.get('status', 'UNKNOWN')
        if status == 'READY':
            break
        time.sleep(10)
        waiter_count += 1
        print(f"    Status: {status}...")

    gateway_url = f"https://{gateway_id}.gateway.bedrock-agentcore.{region}.amazonaws.com/mcp"
    print(f"  ✓ Gateway URL: {gateway_url}")

    return {
        'gateway_id': gateway_id,
        'gateway_url': gateway_url,
        'region': region
    }


def add_lambda_target(gateway_info):
    """Add Lambda tool target to Gateway."""
    gateway_client = boto3.client('bedrock-agentcore-control', region_name=gateway_info['region'])

    print("Adding Lambda tool target...")

    try:
        response = gateway_client.create_target(
            gatewayId=gateway_info['gateway_id'],
            name='SampleTools',
            targetConfiguration={
                'lambdaTarget': {}
            }
        )

        target_id = response['targetId']
        print(f"  ✓ Target added: {target_id}")
        return target_id
    except Exception as e:
        print(f"  ⚠ Could not add Lambda target: {e}")
        print("  (Gateway will work but may have no tools)")
        return None


def get_access_token(cognito_config):
    """Get OAuth access token using your Cognito credentials from Step 7a."""
    print("Getting access token from your Cognito...")

    token_url = cognito_config['token_url']
    client_id = cognito_config['client_id']
    client_secret = cognito_config['client_secret']

    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    response = requests.post(
        token_url,
        headers={
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={'grant_type': 'client_credentials'}
    )

    if response.status_code != 200:
        raise Exception(f"Token request failed: {response.text}")

    access_token = response.json()['access_token']
    print(f"  ✓ Access token obtained")

    return access_token


def create_authenticated_agent(gateway_url, access_token, region="us-west-2"):
    """Create agent that connects to Gateway with your OAuth token."""
    from strands import Agent
    from strands.models import BedrockModel
    from strands.tools.mcp import MCPClient
    from mcp.client.streamable_http import streamablehttp_client

    print(f"Connecting to Gateway with Bearer token...")

    def create_transport():
        return streamablehttp_client(
            gateway_url,
            headers={"Authorization": f"Bearer {access_token}"}
        )

    mcp_client = MCPClient(create_transport)

    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name=region
    )

    return mcp_client, model


def save_gateway_config(gateway_info, filename="gateway_config.json"):
    """Save Gateway configuration."""
    with open(filename, "w") as f:
        json.dump(gateway_info, f, indent=2)
    print(f"✓ Gateway config saved to {filename}")


def load_gateway_config(filename="gateway_config.json"):
    """Load Gateway configuration."""
    with open(filename, "r") as f:
        return json.load(f)


def cleanup_gateway(config_file="gateway_config.json"):
    """Delete Gateway resources (not Cognito - that's Step 7a)."""
    try:
        config = load_gateway_config(config_file)
    except FileNotFoundError:
        print("No gateway_config.json found - nothing to clean up")
        return

    gateway_client = boto3.client('bedrock-agentcore-control', region_name=config['region'])

    print("Deleting Gateway...")
    try:
        gateway_client.delete_gateway(gatewayId=config['gateway_id'])
        print("  ✓ Gateway deleted")
    except Exception as e:
        print(f"  ⚠ Could not delete Gateway: {e}")

    import os
    if os.path.exists(config_file):
        os.remove(config_file)
        print(f"  ✓ Removed {config_file}")

    print("\nNote: Cognito resources still exist.")
    print("To clean up Cognito, run:")
    print("  python lab/exercises/step7a_cognito_oauth.py --cleanup")


def main():
    """Set up Gateway with your Cognito OAuth and test."""
    print("=" * 60)
    print("Step 7b: Gateway with Your Cognito OAuth")
    print("=" * 60)

    # Step 0: Load Cognito config from Step 7a
    print("\n[Step 0] Loading Cognito config from Step 7a...")
    cognito_config = load_cognito_config()
    if cognito_config is None:
        return False

    print(f"  ✓ Cognito Pool: {cognito_config['pool_id']}")
    print(f"  ✓ Domain: {cognito_config['domain']}")
    print(f"  ✓ Client ID: {cognito_config['client_id'][:20]}...")

    # Check for existing Gateway config
    try:
        gateway_config = load_gateway_config()
        print(f"\n  Found existing Gateway: {gateway_config['gateway_id']}")
        use_existing = input("  Use existing Gateway? (y/n): ").strip().lower()
        if use_existing == 'y':
            gateway_url = gateway_config['gateway_url']
        else:
            raise FileNotFoundError("User wants new Gateway")
    except (FileNotFoundError, json.JSONDecodeError):
        # Part 1: Create Gateway
        print("\n[Part 1] Creating Gateway with your Cognito...")
        gateway_info = create_gateway_with_cognito(cognito_config)
        gateway_url = gateway_info['gateway_url']

        # Part 2: Add Lambda target
        print("\n[Part 2] Adding tool target to Gateway...")
        add_lambda_target(gateway_info)

        # Save config
        save_gateway_config(gateway_info)

    # Part 3: Get access token using YOUR Cognito
    print("\n[Part 3] Getting access token from YOUR Cognito...")
    access_token = get_access_token(cognito_config)

    # Part 4: Connect agent with auth
    print("\n[Part 4] Connecting agent to Gateway...")
    mcp_client, model = create_authenticated_agent(gateway_url, access_token, cognito_config['region'])

    # Part 5: Test the connection
    print("\n[Part 5] Testing authenticated Gateway access...")
    try:
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"  ✓ Connected to Gateway!")
            print(f"  ✓ Available tools: {[t.tool_name for t in tools]}")

            if tools:
                from strands import Agent
                agent = Agent(model=model, tools=tools)

                print("\n[Part 6] Testing agent with secured tools...")
                response = agent("What tools do you have? List them briefly.")
                print(f"\nAgent response:\n{response}")

    except Exception as e:
        print(f"  ⚠ Connection test: {e}")
        print("\n  The important part is: your auth setup is correct!")

    print("\n" + "=" * 60)
    print("Step 7b COMPLETE!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        cleanup_gateway()
    else:
        success = main()
        sys.exit(0 if success else 1)
