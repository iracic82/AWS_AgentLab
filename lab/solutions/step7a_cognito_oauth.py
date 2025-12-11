"""
Step 7a: Set Up OAuth Authentication with Amazon Cognito - SOLUTION
===================================================================
"""

import sys
import json
import base64
import requests
import time
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# PART 1: Import boto3
import boto3


def create_cognito_user_pool(pool_name, region="us-west-2"):
    """Create Cognito User Pool for OAuth authentication."""
    cognito = boto3.client('cognito-idp', region_name=region)

    # Step 1: Create User Pool
    print(f"Creating User Pool: {pool_name}...")
    pool_response = cognito.create_user_pool(
        PoolName=pool_name,
        AutoVerifiedAttributes=['email'],
        MfaConfiguration='OFF',
        AdminCreateUserConfig={
            'AllowAdminCreateUserOnly': True  # No self-signup
        }
    )
    pool_id = pool_response['UserPool']['Id']
    print(f"  ✓ User Pool created: {pool_id}")

    return cognito, pool_id


def create_cognito_domain(cognito, pool_id, domain_prefix):
    """Create domain for OAuth endpoints."""
    print(f"Creating domain: {domain_prefix}...")

    cognito.create_user_pool_domain(
        Domain=domain_prefix,
        UserPoolId=pool_id
    )

    print(f"  ✓ Domain created: {domain_prefix}")
    return domain_prefix


def create_resource_server(cognito, pool_id, identifier="agentcore-gateway"):
    """Create Resource Server with scopes."""
    print(f"Creating Resource Server: {identifier}...")

    cognito.create_resource_server(
        UserPoolId=pool_id,
        Identifier=identifier,
        Name="AgentCore Gateway API",
        Scopes=[
            {
                'ScopeName': 'invoke',
                'ScopeDescription': 'Invoke tools via Gateway'
            },
            {
                'ScopeName': 'read',
                'ScopeDescription': 'Read tool information'
            }
        ]
    )

    print(f"  ✓ Resource Server created with scopes: invoke, read")
    return identifier


def create_app_client(cognito, pool_id, client_name, resource_server_id):
    """Create App Client for machine-to-machine auth."""
    print(f"Creating App Client: {client_name}...")

    response = cognito.create_user_pool_client(
        UserPoolId=pool_id,
        ClientName=client_name,
        GenerateSecret=True,  # Required for client_credentials flow
        AllowedOAuthFlows=['client_credentials'],  # M2M flow
        AllowedOAuthScopes=[
            f'{resource_server_id}/invoke',
            f'{resource_server_id}/read'
        ],
        AllowedOAuthFlowsUserPoolClient=True
    )

    client_id = response['UserPoolClient']['ClientId']
    client_secret = response['UserPoolClient']['ClientSecret']

    print(f"  ✓ App Client created: {client_id[:20]}...")

    return client_id, client_secret


def get_access_token(domain, region, client_id, client_secret):
    """Get OAuth access token using client credentials flow."""
    print("Requesting access token...")

    # Build token endpoint URL
    token_url = f"https://{domain}.auth.{region}.amazoncognito.com/oauth2/token"

    # Encode credentials as Base64 (HTTP Basic Auth)
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Make token request
    response = requests.post(
        token_url,
        headers={
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'client_credentials'
        }
    )

    if response.status_code != 200:
        raise Exception(f"Token request failed: {response.text}")

    token_data = response.json()
    access_token = token_data['access_token']
    expires_in = token_data['expires_in']

    print(f"  ✓ Access token obtained (expires in {expires_in}s)")

    return access_token


def save_cognito_config(config, filename="cognito_config.json"):
    """Save Cognito configuration for Step 7b."""
    with open(filename, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✓ Configuration saved to {filename}")


def load_cognito_config(filename="cognito_config.json"):
    """Load Cognito configuration."""
    with open(filename, "r") as f:
        return json.load(f)


def cleanup_cognito(config_file="cognito_config.json"):
    """Delete Cognito resources."""
    config = load_cognito_config(config_file)
    cognito = boto3.client('cognito-idp', region_name=config['region'])

    pool_id = config['pool_id']

    print("Cleaning up Cognito resources...")

    # Delete domain first
    print("  Deleting domain...")
    try:
        cognito.delete_user_pool_domain(
            Domain=config['domain'],
            UserPoolId=pool_id
        )
    except Exception as e:
        print(f"  Warning: Could not delete domain: {e}")

    # Delete User Pool (this deletes clients and resource servers too)
    print("  Deleting User Pool...")
    try:
        cognito.delete_user_pool(UserPoolId=pool_id)
    except Exception as e:
        print(f"  Warning: Could not delete User Pool: {e}")

    # Remove config file
    import os
    if os.path.exists(config_file):
        os.remove(config_file)
        print(f"  Removed {config_file}")

    print("✓ Cleanup complete!")


def main():
    """Set up Cognito OAuth and test token generation."""
    print("=" * 60)
    print("Step 7a: Cognito OAuth Setup")
    print("=" * 60)

    region = "us-west-2"
    pool_name = "DevOpsAgentPool"

    # Generate unique domain prefix
    domain_prefix = f"devops-agent-{int(time.time()) % 100000}"

    # Check if already configured
    try:
        config = load_cognito_config()
        print(f"\nFound existing configuration!")
        print(f"Pool ID: {config['pool_id']}")
        print(f"Domain: {config['domain']}")
        use_existing = input("\nUse existing config? (y/n): ").strip().lower()
        if use_existing == 'y':
            print("\n[Part 6] Testing token generation...")
            access_token = get_access_token(
                config['domain'],
                config['region'],
                config['client_id'],
                config['client_secret']
            )
            if access_token:
                print(f"\n✓ Token obtained successfully!")
                print(f"  Token preview: {access_token[:50]}...")
                return True
            return False
        else:
            print("\nCleaning up old configuration...")
            cleanup_cognito()
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Part 1: Create User Pool
    print("\n[Part 1] Creating Cognito User Pool...")
    cognito, pool_id = create_cognito_user_pool(pool_name, region)

    # Part 2: Create Domain
    print("\n[Part 2] Creating OAuth Domain...")
    domain = create_cognito_domain(cognito, pool_id, domain_prefix)

    # Part 3: Create Resource Server
    print("\n[Part 3] Creating Resource Server...")
    resource_server_id = create_resource_server(cognito, pool_id)

    # Part 4: Create App Client
    print("\n[Part 4] Creating App Client...")
    client_id, client_secret = create_app_client(
        cognito, pool_id, "DevOpsAgentClient", resource_server_id
    )

    # Save configuration
    config = {
        'region': region,
        'pool_id': pool_id,
        'pool_name': pool_name,
        'domain': domain_prefix,
        'resource_server_id': resource_server_id,
        'client_id': client_id,
        'client_secret': client_secret,
        'token_url': f"https://{domain_prefix}.auth.{region}.amazoncognito.com/oauth2/token"
    }
    save_cognito_config(config)

    # Part 5: Test token generation
    print("\n[Part 5] Testing OAuth Token Generation...")
    access_token = get_access_token(domain_prefix, region, client_id, client_secret)

    # Decode and show token info
    print("\n[Part 6] Examining the Access Token (JWT)...")
    try:
        parts = access_token.split('.')
        if len(parts) == 3:
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            decoded = json.loads(base64.b64decode(payload))

            print(f"  Token Type: JWT (JSON Web Token)")
            print(f"  Issuer: {decoded.get('iss', 'N/A')}")
            print(f"  Client ID: {decoded.get('client_id', 'N/A')}")
            print(f"  Scopes: {decoded.get('scope', 'N/A')}")
            print(f"  Expires: {decoded.get('exp', 'N/A')}")
    except Exception as e:
        print(f"  Could not decode token: {e}")

    print("\n" + "=" * 60)
    print("Step 7a COMPLETE!")
    print("=" * 60)
    print(f"""
What you built:
✓ Cognito User Pool ({pool_id})
✓ OAuth Domain ({domain_prefix})
✓ Resource Server with scopes (invoke, read)
✓ App Client with client_credentials flow
✓ Successfully obtained Bearer token!

Next step:
  python lab/exercises/step7b_gateway_auth.py
""")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        cleanup_cognito()
    else:
        success = main()
        sys.exit(0 if success else 1)
