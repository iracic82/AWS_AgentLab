"""
Step 3b: Create an Infoblox CSP IPAM Tool
=========================================
Learn how to integrate with enterprise IPAM systems for network capacity checks.

EXERCISE: Build a tool that checks subnet IP availability in Infoblox CSP
before allowing deployments.

Learning objectives:
- Integrate with Infoblox Cloud Services Portal (CSP) API
- Handle API authentication with tokens
- Parse network utilization data
- Make deployment decisions based on IP capacity

Why check IP capacity before deployment?
- Deployments need IP addresses for new instances
- Running out of IPs causes deployment failures
- Proactive checking prevents outages
- Enterprise networks require IPAM integration

Infoblox CSP API:
- Base URL: https://csp.infoblox.com/api/ddi/v1
- Auth: Token-based (Authorization: Token <api_key>)
- Endpoint: /ipam/subnet for subnet info

Environment Variables Required:
- IPAM_API_KEY: Your Infoblox CSP API key
- IPAM_BASE_URL: (Optional) Custom CSP URL

Run: python lab/exercises/step3b_ipam_tool.py
Test: python lab/tests/test_step3b.py
"""

import os
import requests
from strands import Agent
from strands.tools import tool
from strands.models import BedrockModel


# =============================================================================
# TODO 1: Create the IPAM tool function
# =============================================================================

# The tool should:
#   - Take a region/subnet identifier as input
#   - Connect to Infoblox CSP API
#   - Get subnet utilization data
#   - Return capacity info (total IPs, used, available, utilization %)
#
# Hint:
# @tool
# def check_subnet_capacity(region: str, min_required_ips: int = 10) -> dict:
#     """
#     Check if a subnet has enough available IP addresses for deployment.
#
#     Args:
#         region: The region/subnet identifier to check (e.g., "us-west-2", "prod-vpc-1")
#         min_required_ips: Minimum number of free IPs needed for deployment (default: 10)
#
#     Returns:
#         Dictionary with subnet capacity info and deployment recommendation
#     """
#     api_key = os.getenv("IPAM_API_KEY")
#     base_url = os.getenv("IPAM_BASE_URL", "https://csp.infoblox.com/api/ddi/v1")
#
#     if not api_key:
#         return {
#             "status": "error",
#             "message": "IPAM_API_KEY not configured",
#             "recommendation": "CAUTION - Cannot verify IP capacity"
#         }
#
#     try:
#         # Query Infoblox CSP for subnet info
#         headers = {
#             "Authorization": f"Token {api_key}",
#             "Content-Type": "application/json"
#         }
#
#         # Search for subnet by region tag or name
#         response = requests.get(
#             f"{base_url}/ipam/subnet",
#             headers=headers,
#             params={"_filter": f"tags~'{region}' or comment~'{region}'"},
#             timeout=10
#         )
#         response.raise_for_status()
#
#         data = response.json()
#         subnets = data.get("results", [])
#
#         if not subnets:
#             return {
#                 "region": region,
#                 "status": "not_found",
#                 "message": f"No subnet found for region: {region}",
#                 "recommendation": "CAUTION - Subnet not in IPAM"
#             }
#
#         # Aggregate capacity across matching subnets
#         total_ips = 0
#         used_ips = 0
#         available_ips = 0
#
#         for subnet in subnets:
#             util = subnet.get("utilization", {})
#             total_ips += util.get("total", 0)
#             used_ips += util.get("used", 0)
#             available_ips += util.get("available", 0)
#
#         utilization_percent = (used_ips / total_ips * 100) if total_ips > 0 else 0
#
#         # Determine recommendation
#         if available_ips >= min_required_ips and utilization_percent < 80:
#             recommendation = "GO"
#             status = "healthy"
#         elif available_ips >= min_required_ips:
#             recommendation = "CAUTION"
#             status = "warning"
#         else:
#             recommendation = "NO-GO"
#             status = "critical"
#
#         return {
#             "region": region,
#             "status": status,
#             "total_ips": total_ips,
#             "used_ips": used_ips,
#             "available_ips": available_ips,
#             "utilization_percent": round(utilization_percent, 1),
#             "min_required": min_required_ips,
#             "recommendation": recommendation,
#             "message": f"{available_ips} IPs available ({utilization_percent:.1f}% utilized)"
#         }
#
#     except requests.exceptions.RequestException as e:
#         return {
#             "region": region,
#             "status": "error",
#             "message": f"IPAM API error: {str(e)}",
#             "recommendation": "CAUTION - Could not verify IP capacity"
#         }

@tool
def check_subnet_capacity(region: str, min_required_ips: int = 10) -> dict:
    """
    Check if a subnet has enough available IP addresses for deployment.

    Args:
        region: The region/subnet identifier to check (e.g., "us-west-2", "prod-vpc-1")
        min_required_ips: Minimum number of free IPs needed for deployment (default: 10)

    Returns:
        Dictionary with subnet capacity info and deployment recommendation
    """
    # TODO: Implement this function following the hint above
    pass


# =============================================================================
# TODO 2: Create a mock version for testing without CSP access
# =============================================================================

# For lab environments without Infoblox CSP access, create a mock that
# simulates realistic responses.
#
# Hint:
# def get_mock_subnet_data(region: str) -> dict:
#     """Return mock subnet data for testing."""
#     mock_data = {
#         "us-west-2": {"total": 256, "used": 45, "available": 211},
#         "us-east-1": {"total": 512, "used": 489, "available": 23},  # Almost full!
#         "eu-west-1": {"total": 128, "used": 120, "available": 8},   # Critical!
#         "ap-southeast-1": {"total": 256, "used": 100, "available": 156},
#     }
#     return mock_data.get(region, {"total": 256, "used": 128, "available": 128})

def get_mock_subnet_data(region: str) -> dict:
    """Return mock subnet data for testing."""
    # TODO: Implement mock data for different regions
    pass


# =============================================================================
# TODO 3: Update the tool to use mock data when IPAM_API_KEY is not set
# =============================================================================

# Modify check_subnet_capacity to fall back to mock data when no API key
# This allows the lab to work without real Infoblox access
#
# Add this at the start of check_subnet_capacity:
#
#     # Use mock data if no API key (for lab/testing)
#     if not api_key:
#         mock = get_mock_subnet_data(region)
#         available = mock["available"]
#         utilization = (mock["used"] / mock["total"] * 100) if mock["total"] > 0 else 0
#
#         if available >= min_required_ips and utilization < 80:
#             recommendation = "GO"
#             status = "healthy"
#         elif available >= min_required_ips:
#             recommendation = "CAUTION"
#             status = "warning"
#         else:
#             recommendation = "NO-GO"
#             status = "critical"
#
#         return {
#             "region": region,
#             "status": status,
#             "total_ips": mock["total"],
#             "used_ips": mock["used"],
#             "available_ips": available,
#             "utilization_percent": round(utilization, 1),
#             "min_required": min_required_ips,
#             "recommendation": recommendation,
#             "message": f"{available} IPs available ({utilization:.1f}% utilized)",
#             "source": "mock_data"  # Indicates this is simulated
#         }


def test_ipam_tool():
    """Test the IPAM tool."""
    print("Testing IPAM tool...")

    # Test different regions
    test_regions = ["us-west-2", "us-east-1", "eu-west-1", "ap-southeast-1"]

    for region in test_regions:
        print(f"\nChecking {region}...")
        result = check_subnet_capacity(region)

        if result is None:
            print(f"  ERROR: Tool returned None. Complete the TODOs!")
            return False

        print(f"  Status: {result.get('status', 'unknown')}")
        print(f"  Available IPs: {result.get('available_ips', 'N/A')}")
        print(f"  Utilization: {result.get('utilization_percent', 'N/A')}%")
        print(f"  Recommendation: {result.get('recommendation', 'N/A')}")

    return True


def main():
    """Test the IPAM tool with an agent."""
    print("=" * 60)
    print("Step 3b: Infoblox CSP IPAM Tool")
    print("=" * 60)

    # First test the tool directly
    if not test_ipam_tool():
        print("\nERROR: Complete the TODOs first!")
        return

    print("\n" + "=" * 60)
    print("Testing with Agent")
    print("=" * 60)

    # Create agent with the IPAM tool
    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-west-2"
    )

    agent = Agent(model=model, tools=[check_subnet_capacity])

    # Test the agent
    response = agent("Check if us-east-1 has enough IP capacity for a deployment that needs 50 IPs")
    print(f"\nAgent response:\n{response}")


if __name__ == "__main__":
    main()
