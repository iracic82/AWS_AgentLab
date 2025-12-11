# DevOps Decision Agent Lab

Build and deploy an AI agent using **Strands Agents SDK**, **MCP**, and **AWS AgentCore**.

## What You'll Build

A DevOps Decision Agent that helps engineers decide if it's safe to deploy by checking:
- AWS service health status
- Weather conditions in datacenter regions
- IP address capacity (via Infoblox CSP IPAM)
- External service status (via MCP)

The agent gives **GO / CAUTION / NO-GO** deployment recommendations.

## Prerequisites

- Python 3.10+
- AWS account with Bedrock access (Claude models enabled in us-west-2)
- AWS CLI configured (`aws configure`)
- uv/uvx installed (for MCP server)
- (Optional) Infoblox CSP API key for real IPAM integration

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd AWS_AgentLab
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start with Step 1!
python lab/exercises/step1_hello_agent.py
```

## Lab Structure

This lab uses a **coding exercise** approach:

```
lab/
├── exercises/          # YOUR workspace - complete the TODOs here
├── solutions/          # Reference solutions (try not to peek!)
└── tests/              # Validation tests to check your work
```

**Workflow for each step:**
1. Open the exercise file and complete the TODOs
2. Run the exercise file to test your implementation
3. Run the test file to validate your work
4. If stuck, check the solution file for hints

---

## Lab Steps

### Step 1: Hello World Agent (Verify Setup)

**Exercise:** `lab/exercises/step1_hello_agent.py`

Complete the TODOs to create your first agent with Strands SDK.

```bash
# Run your implementation
python lab/exercises/step1_hello_agent.py

# Validate your work
python lab/tests/test_step1.py
```

**Learning:** Basic agent creation with BedrockModel.

---

### Step 2: Build a Weather Tool

**Exercise:** `lab/exercises/step2_weather_tool.py`

Complete the TODOs to create a custom tool using the `@tool` decorator.

```bash
python lab/exercises/step2_weather_tool.py
python lab/tests/test_step2.py
```

**Learning:** Creating custom tools with `@tool` decorator, API integration.

---

### Step 3: Build an AWS Status Tool

**Exercise:** `lab/exercises/step3_aws_status_tool.py`

Complete the TODOs to create a tool that checks AWS service health.

```bash
python lab/exercises/step3_aws_status_tool.py
python lab/tests/test_step3.py
```

**Learning:** XML/RSS parsing, creating operational tools.

---

### Step 3b: Build an IPAM Tool (Infoblox CSP)

**Exercise:** `lab/exercises/step3b_ipam_tool.py`

Complete the TODOs to create a tool that checks subnet IP capacity.

```bash
# Optional: Set Infoblox API key for real integration
export IPAM_API_KEY=your_api_key

# Run your implementation (uses mock data if no API key)
python lab/exercises/step3b_ipam_tool.py
python lab/tests/test_step3b.py
```

**Learning:** Enterprise IPAM integration, network capacity planning, API authentication.

**Why check IP capacity?**
- Deployments need IP addresses for new instances
- Running out of IPs causes deployment failures
- Enterprise networks require IPAM integration

---

### Step 4: MCP Integration

**Exercise:** `lab/exercises/step4_mcp_integration.py`

Complete the TODOs to connect your agent to external MCP tools.

```bash
python lab/exercises/step4_mcp_integration.py
python lab/tests/test_step4.py
```

**Learning:** MCP protocol, connecting to external tool servers.

---

### Step 5: Design Your Agent's Personality

**Exercise:** `lab/exercises/step5_system_prompt.py`

Complete the TODOs to write a system prompt and create the complete DevOps agent.

```bash
python lab/exercises/step5_system_prompt.py
python lab/tests/test_step5.py
```

**Learning:** System prompts, agent personality design, structured output.

---

### Step 6: Deploy to AWS AgentCore

**Exercise:** `lab/exercises/step6_agentcore_handler.py`

Complete the TODOs to create the AgentCore handler for cloud deployment.

```bash
# Run your implementation locally
python lab/exercises/step6_agentcore_handler.py

# Validate your work
python lab/tests/test_step6.py

# Deploy to AgentCore
agentcore configure -e lab/exercises/step6_agentcore_handler.py \
    -r us-west-2 --disable-memory -n devops_agent

agentcore deploy

# Test the deployed agent
agentcore invoke '{"prompt": "Should I deploy to us-east-1?"}'

# Cleanup when done
agentcore destroy
```

**Learning:** AgentCore architecture, serverless deployment, cloud packaging.

---

### Step 7a: Set Up OAuth with Amazon Cognito

**Exercise:** `lab/exercises/step7a_cognito_oauth.py`

Learn OAuth 2.0 by manually creating a Cognito User Pool with client credentials flow.

```bash
# Validate your code structure
python lab/tests/test_step7a.py

# Run the exercise (creates Cognito resources)
python lab/exercises/step7a_cognito_oauth.py
```

**Learning:** OAuth 2.0 client credentials flow, Cognito User Pools, JWT tokens.

---

### Step 7b: Connect Gateway to Your Cognito

**Exercise:** `lab/exercises/step7b_gateway_auth.py`

Use YOUR Cognito from Step 7a to secure AgentCore Gateway.

```bash
# Validate your code structure
python lab/tests/test_step7b.py

# Run the exercise (creates Gateway with YOUR Cognito)
python lab/exercises/step7b_gateway_auth.py

# Cleanup when done
python lab/exercises/step7b_gateway_auth.py --cleanup  # Gateway
python lab/exercises/step7a_cognito_oauth.py --cleanup  # Cognito
```

**Learning:** AgentCore Gateway, JWT validation, end-to-end OAuth flow.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DevOps Decision Agent                        │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │  Weather   │  │ AWS Status │  │   IPAM     │  │    MCP     │ │
│  │   Tool     │  │   Tool     │  │   Tool     │  │   Tools    │ │
│  │ (Step 2)   │  │ (Step 3)   │  │ (Step 3b)  │  │ (Step 4)   │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              System Prompt (Step 5)                       │   │
│  │         GO / CAUTION / NO-GO Recommendations              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS AgentCore (Step 6)                        │
│                   Serverless Cloud Deployment                    │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                OAuth Security (Steps 7a & 7b)                    │
│          Cognito + Gateway Bearer Token Authentication           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AWS_PROFILE` | AWS CLI profile to use | Yes (if not default) |
| `AWS_REGION` | Default AWS region | No (defaults to us-west-2) |
| `IPAM_API_KEY` | Infoblox CSP API key | No (uses mock data) |
| `IPAM_BASE_URL` | Infoblox CSP base URL | No (defaults to CSP) |

---

## Cleanup

```bash
# Remove AgentCore deployment
agentcore destroy

# Remove Gateway (if created in Step 7b)
python lab/exercises/step7b_gateway_auth.py --cleanup

# Remove Cognito resources (if created in Step 7a)
python lab/exercises/step7a_cognito_oauth.py --cleanup
```

---

## Troubleshooting

**Model access error:**
- Ensure Claude models are enabled in AWS Bedrock console for us-west-2
- Check your AWS profile has bedrock permissions

**MCP server not found:**
- Install uvx: `pip install uv`
- MCP server runs via `uvx mcp-server-fetch`

**AgentCore deploy fails:**
- Check AWS credentials: `aws sts get-caller-identity`
- Ensure CodeBuild and ECR permissions

**IPAM tool returns mock data:**
- Set `IPAM_API_KEY` environment variable for real Infoblox integration
- Mock data is fine for learning purposes

---

## Resources

- [Strands Agents SDK](https://github.com/strands-agents/strands)
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [Infoblox CSP API](https://docs.infoblox.com/)
