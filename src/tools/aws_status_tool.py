"""
Custom Tool: AWS Service Status Checker
=======================================
Checks AWS Health Dashboard for service status.
Uses the public AWS status RSS feed.
"""

import requests
from strands.tools import tool


@tool
def check_aws_status(region: str = "us-east-1") -> dict:
    """
    Check AWS service health status for a specific region.
    Useful before deployments to ensure AWS services are healthy.

    Args:
        region: AWS region to check (e.g., "us-east-1", "eu-west-1", "us-west-2")

    Returns:
        Current AWS service status and any ongoing incidents
    """
    try:
        # Use the AWS status RSS feed which is more reliable
        response = requests.get(
            f"https://status.aws.amazon.com/rss/all.rss",
            timeout=10,
            headers={"User-Agent": "DevOpsAgent/1.0"}
        )
        response.raise_for_status()

        # Parse RSS for region-specific issues
        content = response.text.lower()
        region_mentioned = region.lower() in content

        # Check for recent items mentioning the region
        if region_mentioned:
            return {
                "region": region,
                "status": "check_needed",
                "message": f"AWS status feed mentions {region}. Check https://health.aws.amazon.com for details.",
                "recommendation": "Review AWS Health Dashboard before deploying"
            }
        else:
            return {
                "region": region,
                "status": "healthy",
                "message": f"No recent issues found for {region} in AWS status feed.",
                "recommendation": "Safe to proceed with deployment"
            }

    except requests.RequestException as e:
        return {
            "region": region,
            "status": "unknown",
            "message": f"Could not fetch AWS status. Check https://health.aws.amazon.com manually.",
            "error": str(e)
        }
