"""
Shared configuration for the DevOps Decision Agent.
"""

from strands.models import BedrockModel

# Default model configuration
# Claude 3.5 Sonnet v2 - using cross-region inference profile
DEFAULT_MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
DEFAULT_REGION = "us-west-2"


def get_model() -> BedrockModel:
    """Get configured Bedrock model."""
    return BedrockModel(
        model_id=DEFAULT_MODEL_ID,
        region_name=DEFAULT_REGION
    )
