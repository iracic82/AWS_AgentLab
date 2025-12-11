"""
Step 3b Solution: Infoblox CSP IPAM Tool
========================================
Complete implementation of the IPAM subnet capacity checker.
"""

import os
import requests
from strands.tools import tool


def get_mock_subnet_data(region: str) -> dict:
    """Return mock subnet data for testing."""
    mock_data = {
        "us-west-2": {"total": 256, "used": 45, "available": 211},
        "us-east-1": {"total": 512, "used": 489, "available": 23},  # Almost full!
        "eu-west-1": {"total": 128, "used": 120, "available": 8},   # Critical!
        "ap-southeast-1": {"total": 256, "used": 100, "available": 156},
    }
    return mock_data.get(region, {"total": 256, "used": 128, "available": 128})


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
    api_key = os.getenv("IPAM_API_KEY")
    base_url = os.getenv("IPAM_BASE_URL", "https://csp.infoblox.com/api/ddi/v1")

    # Use mock data if no API key (for lab/testing)
    if not api_key:
        mock = get_mock_subnet_data(region)
        available = mock["available"]
        utilization = (mock["used"] / mock["total"] * 100) if mock["total"] > 0 else 0

        if available >= min_required_ips and utilization < 80:
            recommendation = "GO"
            status = "healthy"
        elif available >= min_required_ips:
            recommendation = "CAUTION"
            status = "warning"
        else:
            recommendation = "NO-GO"
            status = "critical"

        return {
            "region": region,
            "status": status,
            "total_ips": mock["total"],
            "used_ips": mock["used"],
            "available_ips": available,
            "utilization_percent": round(utilization, 1),
            "min_required": min_required_ips,
            "recommendation": recommendation,
            "message": f"{available} IPs available ({utilization:.1f}% utilized)",
            "source": "mock_data"  # Indicates this is simulated
        }

    try:
        # Query Infoblox CSP for subnet info
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }

        # Search for subnet by region tag or name
        response = requests.get(
            f"{base_url}/ipam/subnet",
            headers=headers,
            params={"_filter": f"tags~'{region}' or comment~'{region}'"},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        subnets = data.get("results", [])

        if not subnets:
            return {
                "region": region,
                "status": "not_found",
                "message": f"No subnet found for region: {region}",
                "recommendation": "CAUTION - Subnet not in IPAM"
            }

        # Aggregate capacity across matching subnets
        total_ips = 0
        used_ips = 0
        available_ips = 0

        for subnet in subnets:
            util = subnet.get("utilization", {})
            total_ips += util.get("total", 0)
            used_ips += util.get("used", 0)
            available_ips += util.get("available", 0)

        utilization_percent = (used_ips / total_ips * 100) if total_ips > 0 else 0

        # Determine recommendation
        if available_ips >= min_required_ips and utilization_percent < 80:
            recommendation = "GO"
            status = "healthy"
        elif available_ips >= min_required_ips:
            recommendation = "CAUTION"
            status = "warning"
        else:
            recommendation = "NO-GO"
            status = "critical"

        return {
            "region": region,
            "status": status,
            "total_ips": total_ips,
            "used_ips": used_ips,
            "available_ips": available_ips,
            "utilization_percent": round(utilization_percent, 1),
            "min_required": min_required_ips,
            "recommendation": recommendation,
            "message": f"{available_ips} IPs available ({utilization_percent:.1f}% utilized)"
        }

    except requests.exceptions.RequestException as e:
        return {
            "region": region,
            "status": "error",
            "message": f"IPAM API error: {str(e)}",
            "recommendation": "CAUTION - Could not verify IP capacity"
        }
