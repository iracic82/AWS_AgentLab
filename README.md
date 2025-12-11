# DevOps Decision Agent Lab

Build and deploy a production-ready AI agent using **Strands Agents SDK**, **MCP**, and **AWS Bedrock AgentCore**.

---

## What You'll Build

A DevOps Decision Agent that analyzes multiple factors before deployment and gives a clear **GO / CAUTION / NO-GO** recommendation.

```
User: "Should I deploy to us-east-1?"

Agent: Checking deployment readiness...
  ✓ AWS us-east-1: All services healthy
  ✓ Weather (Virginia): Clear skies, 72°F
  ⚠ IP Capacity: 23 IPs available (95.5% utilized)

RECOMMENDATION: CAUTION
Proceed with deployment but monitor IP capacity.
```

| Check | Why It Matters |
|-------|----------------|
| **AWS Service Health** | Don't deploy during AWS outages |
| **Weather Conditions** | Severe weather can affect datacenters |
| **IP Address Capacity** | Deployments fail without available IPs |

---

## Prerequisites

- **Python 3.10+**
- **AWS Account** with Bedrock access and Claude models enabled
- **AWS CLI configured** - verify with `aws sts get-caller-identity`

---

## Quick Start

```bash
git clone https://github.com/iracic82/AWS_AgentLab.git
cd AWS_AgentLab
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the lab
python lab/exercises/step1_hello_agent.py
```

---

## Lab Steps

Each step has an **exercise** (with TODOs), **solution**, and **test** file.

| Step | What You'll Build | Key Concepts |
|------|-------------------|--------------|
| **1** | Hello World Agent | Strands SDK, BedrockModel, Agent basics |
| **2** | Weather Tool | `@tool` decorator, HTTP APIs, structured data |
| **3** | AWS Status Tool | RSS parsing, deployment decisions, multi-tool agents |
| **3b** | IPAM Tool | Enterprise integration, Infoblox CSP, mock data |
| **4** | MCP Integration | Model Context Protocol, local MCP servers |
| **5** | System Prompt | Agent personality, response format, guardrails |
| **6** | AgentCore Deploy | `@app.entrypoint`, agentcore CLI, cloud deployment |
| **7a** | Cognito OAuth | OAuth 2.0, client credentials flow, JWT tokens |
| **7b** | Gateway Auth | AgentCore Gateway, remote MCP, secure APIs |

### Running Each Step

```bash
# Edit and complete the TODOs
code lab/exercises/step1_hello_agent.py

# Run your implementation
python lab/exercises/step1_hello_agent.py

# Validate with test
python lab/tests/test_step1.py

# If stuck, check the solution
cat lab/solutions/step1_hello_agent.py
```

---

## What is an AI Agent?

An **AI Agent** = LLM + Tools + System Prompt

| Component | Purpose |
|-----------|---------|
| **LLM Model** | The "brain" - reasons, decides when/which tools to use |
| **System Prompt** | The "instructions" - defines role, behavior, response format |
| **Tools** | The "capabilities" - fetch data, take actions, interact with systems |

**Without tools**: LLM can only respond based on training data.
**With tools**: Agent can call APIs, query databases, take real actions.

```
┌─────────────────────────────────────────────────────────────────┐
│                         AI AGENT                                 │
│                                                                  │
│   ┌─────────────────┐                                           │
│   │   LLM MODEL     │  ← Decides WHEN and WHICH tools to use   │
│   └────────┬────────┘                                           │
│            │                                                     │
│   ┌────────▼────────┐                                           │
│   │  SYSTEM PROMPT  │  ← Defines role, behavior, format        │
│   └────────┬────────┘                                           │
│            │                                                     │
│   ┌────────▼────────┐                                           │
│   │     TOOLS       │  ← Execute and return data               │
│   │  [aws_status]   │                                           │
│   │  [weather]      │                                           │
│   │  [ipam_check]   │                                           │
│   └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why Strands Agents SDK?

**Old Way (Bedrock Agents + Lambda):**
- Lambda function per tool
- Cold start latency
- Complex IAM roles
- Hard to test locally

**New Way (Strands SDK):**
```python
from strands import Agent
from strands.tools import tool

@tool
def check_aws_status(region: str) -> dict:
    """Check AWS service health."""
    return {"status": "healthy", "region": region}

agent = Agent(tools=[check_aws_status])
response = agent("Is AWS healthy in us-east-1?")
```

✅ Simple `@tool` decorator
✅ Test locally first
✅ Single deployment
✅ Works with any LLM

---

## Why AWS AgentCore?

**Traditional AWS**: You manage API Gateway, Lambda, IAM, WAF, CloudWatch, scaling...

**AgentCore**: You manage your agent code. That's it.

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENTCORE                                 │
│                                                                  │
│   Client ──▶ AgentCore Runtime ──▶ Your Agent Code              │
│                     │                                            │
│         ┌───────────┼───────────┐                               │
│         ▼           ▼           ▼                               │
│    ✅ Auth     ✅ Scale    ✅ Logs                              │
│    ✅ Memory   ✅ Policy   ✅ Gateway                           │
│                                                                  │
│   YOU MANAGE: Your agent code. That's it.                       │
└─────────────────────────────────────────────────────────────────┘
```

| Feature | Traditional | AgentCore |
|---------|-------------|-----------|
| HTTP Endpoint | API Gateway setup | ✅ Automatic |
| Authentication | Cognito + config | ✅ Built-in |
| Cold Start | Seconds | ✅ Milliseconds |
| Scaling | Manual config | ✅ Automatic |
| Logging | CloudWatch setup | ✅ Automatic |

**Deploy in 3 commands:**
```bash
agentcore configure -e handler.py -r us-west-2 -n my_agent
agentcore deploy
agentcore invoke '{"prompt": "Should I deploy?"}'
```

---

## What is MCP?

**MCP (Model Context Protocol)** is an open standard for connecting AI to tools.

**Problem**: Every AI framework has its own tool format (LangChain, OpenAI, Bedrock...).
**Solution**: MCP standardizes tool communication - write once, use anywhere.

**This lab uses both approaches:**
- **Direct `@tool`** - Simple tools specific to your agent (Steps 2, 3, 3b)
- **MCP servers** - Reusable tools via standard protocol (Step 4)

### Local vs Remote MCP

| Type | Transport | Use Case | Lab Step |
|------|-----------|----------|----------|
| **Local** | stdio (pipes) | Development, single machine | Step 4 |
| **Remote** | HTTPS + OAuth | Production, shared access | Step 7b |

```python
# Local MCP (Step 4)
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uvx", args=["mcp-server-fetch"])
))

# Remote MCP (Step 7b)
mcp_client = MCPClient(lambda: streamablehttp_client(
    "https://gateway.agentcore.amazonaws.com/mcp",
    headers={"Authorization": f"Bearer {token}"}
))
```

---

## AgentCore Capabilities

| Capability | What It Does |
|------------|--------------|
| **Runtime** | Firecracker microVMs, millisecond cold starts |
| **Memory** | Short & long-term memory across sessions |
| **Gateways** | MCP, OpenAPI, Lambda tool access |
| **Identity** | OAuth/JWT authentication |
| **Policy** | Cedar-based authorization (who can do what) |
| **Observability** | Built-in monitoring and debugging |

---

## Cleanup

**Important**: Clean up AWS resources when done!

```bash
agentcore destroy
python lab/exercises/step7b_gateway_auth.py --cleanup
python lab/exercises/step7a_cognito_oauth.py --cleanup
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AWS_PROFILE` | AWS CLI profile | If not default |
| `AWS_REGION` | AWS region | No (defaults to us-west-2) |
| `IPAM_API_KEY` | Infoblox CSP API key | No (uses mock data) |

---

## Resources

- [Strands Agents SDK](https://github.com/strands-agents/strands)
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Model Context Protocol](https://modelcontextprotocol.io)
