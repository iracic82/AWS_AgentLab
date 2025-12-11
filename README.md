# DevOps Decision Agent Lab

Build and deploy a production-ready AI agent using **Strands Agents SDK**, **MCP**, and **AWS Bedrock AgentCore**.

---

## What is an AI Agent?

An **AI Agent** is an autonomous system that can reason, plan, and take actions to accomplish goals.

### LLM vs Agent: The Key Difference

| Capability | LLM Alone | Agent (LLM + Tools) |
|------------|-----------|---------------------|
| Answer questions | ✅ Based on training data only | ✅ Can fetch real-time data |
| Access current information | ❌ Knowledge cutoff date | ✅ Query APIs, databases, web |
| Take actions | ❌ Can only generate text | ✅ Create tickets, send alerts, deploy code |
| Multi-step reasoning | ⚠️ Limited to single response | ✅ Plan → Execute → Observe → Iterate |

**Without tools**: An LLM can only respond based on what it learned during training. Ask it "What's the weather in Seattle?" and it will say "I don't have access to real-time data."

**With tools**: An agent can call a weather API, get current conditions, and give you an accurate answer.

### The Three Components of an AI Agent

```
┌─────────────────────────────────────────────────────────────────┐
│                         AI AGENT                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    1. LLM MODEL                          │    │
│  │                                                          │    │
│  │   The "brain" that:                                      │    │
│  │   • Understands natural language                         │    │
│  │   • Reasons about problems                               │    │
│  │   • Decides WHEN to use tools                            │    │
│  │   • Decides WHICH tool to use                            │    │
│  │   • Interprets tool results                              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  2. SYSTEM PROMPT                        │    │
│  │                                                          │    │
│  │   The "instructions" that define:                        │    │
│  │   • Agent's role and expertise                           │    │
│  │   • How to approach problems                             │    │
│  │   • Response format and style                            │    │
│  │   • Constraints and guardrails                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     3. TOOLS                             │    │
│  │                                                          │    │
│  │   The "capabilities" that allow the agent to:            │    │
│  │   • Fetch real-time data (APIs, databases)               │    │
│  │   • Take actions (create, update, delete)                │    │
│  │   • Interact with external systems                       │    │
│  │                                                          │    │
│  │   [check_aws_status] [get_weather] [query_ipam]          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Example: How an Agent Uses Tools

```
User: "Should I deploy to us-east-1?"

Agent's reasoning (internal):
1. "I need to check if it's safe to deploy"
2. "I should check AWS service health" → calls check_aws_status("us-east-1")
3. "I should check IP capacity" → calls check_subnet_capacity("us-east-1")
4. "Let me analyze the results and give a recommendation"

Agent's response:
"Based on my checks:
 ✓ AWS us-east-1: All services healthy
 ⚠ IP Capacity: Only 23 IPs available (95% utilized)

 RECOMMENDATION: CAUTION - Proceed but request more IPs soon."
```

The LLM **decides** when and which tools to call. The tools **execute** and return data. The LLM **interprets** results and responds.

---

## What is MCP (Model Context Protocol)?

**MCP** is an open standard (created by Anthropic) for connecting AI models to external tools and data sources.

### The Problem MCP Solves

Before MCP, every AI framework had its own tool format:
- LangChain tools
- OpenAI function calling
- Bedrock Agent action groups
- Custom implementations

This meant **rewriting the same tool for every framework**.

### How MCP Works

MCP defines a standard protocol for tool communication:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Architecture                              │
│                                                                  │
│   ┌─────────────┐                    ┌─────────────────┐        │
│   │   Your App  │                    │   MCP Server    │        │
│   │   (Agent)   │◀──── MCP ─────────▶│   (Tool Host)   │        │
│   │             │    Protocol        │                 │        │
│   └─────────────┘                    └─────────────────┘        │
│         │                                    │                   │
│         │ "list tools"                       │                   │
│         │ "call tool X"                      ▼                   │
│         │ "get result"              ┌───────────────┐           │
│         │                           │  External     │           │
│         └──────────────────────────▶│  Services     │           │
│                                     │  (APIs, DBs)  │           │
│                                     └───────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### MCP Benefits

| Benefit | Description |
|---------|-------------|
| **Write Once, Use Anywhere** | Build a tool server once, connect from any MCP client |
| **Standardized Discovery** | Agents can discover available tools automatically |
| **Language Agnostic** | Tool servers can be written in any language |
| **Ecosystem** | Growing library of pre-built MCP servers |

### MCP vs Direct Tool Integration

| Approach | When to Use |
|----------|-------------|
| **Direct `@tool`** | Simple, single-use tools specific to your agent |
| **MCP Server** | Reusable tools shared across multiple agents/apps |

**This lab uses both approaches** - direct tools for custom logic, MCP for standardized external tools.

---

## Why This Lab?

AI agents are transforming how we automate complex workflows. But building production-ready agents requires more than just calling an LLM - you need:

- **Tool orchestration** - Agents that can use multiple tools intelligently
- **Enterprise integrations** - Connect to real systems (IPAM, monitoring, etc.)
- **Cloud deployment** - Scalable, secure, production-grade hosting
- **Guardrails** - Prevent harmful outputs, ensure compliance
- **Authentication** - OAuth 2.0, API security, access control

This lab teaches all of that by building a **DevOps Decision Agent** that helps engineers decide if it's safe to deploy.

---

## What You'll Build

A DevOps Decision Agent that analyzes multiple factors before deployment:

| Check | Why It Matters |
|-------|----------------|
| **AWS Service Health** | Don't deploy during AWS outages |
| **Weather Conditions** | Severe weather can affect datacenters |
| **IP Address Capacity** | Deployments fail without available IPs |
| **External Services** | Check GitHub, dependencies status |

The agent synthesizes all data and gives a clear **GO / CAUTION / NO-GO** recommendation.

```
User: "Should I deploy to us-east-1?"

Agent: Checking deployment readiness...
  ✓ AWS us-east-1: All services healthy
  ✓ Weather (Virginia): Clear skies, 72°F
  ⚠ IP Capacity: 23 IPs available (95.5% utilized)

RECOMMENDATION: CAUTION
Proceed with deployment but monitor IP capacity.
Consider requesting additional subnet allocation.
```

---

## Why Strands Agents vs Bedrock Agents (Lambda)?

### The Old Way: Bedrock Agents with Lambda

Traditional Bedrock Agents require:
- Writing Lambda functions for each tool
- Managing Lambda cold starts (latency!)
- Complex IAM roles per function
- Manual orchestration logic
- Separate deployment for each tool

```
┌─────────────────────────────────────────────────────────────┐
│                    Bedrock Agent (Lambda)                    │
│                                                              │
│   Agent ──▶ Lambda1 ──▶ Lambda2 ──▶ Lambda3                 │
│              │            │            │                     │
│           IAM Role     IAM Role     IAM Role                │
│           Cold Start   Cold Start   Cold Start              │
│                                                              │
│   ❌ Complex setup                                           │
│   ❌ Cold start latency                                      │
│   ❌ IAM role per function                                   │
│   ❌ Hard to test locally                                    │
└─────────────────────────────────────────────────────────────┘
```

### The New Way: Strands Agents SDK

Strands gives you:
- **Simple `@tool` decorator** - Turn any Python function into an agent tool
- **Local development** - Test everything on your laptop first
- **Single deployment** - All tools packaged together
- **Model flexibility** - Works with any LLM (Bedrock, OpenAI, local)

```python
from strands import Agent
from strands.tools import tool

@tool
def check_aws_status(region: str) -> dict:
    """Check AWS service health for a region."""
    # Your logic here - no Lambda needed!
    return {"status": "healthy", "region": region}

# That's it! The agent can now use this tool
agent = Agent(tools=[check_aws_status])
response = agent("Is AWS healthy in us-east-1?")
```

```
┌─────────────────────────────────────────────────────────────┐
│                    Strands Agent                             │
│                                                              │
│   @tool           @tool           @tool                     │
│   weather()       aws_status()    ipam_check()              │
│        │               │               │                     │
│        └───────────────┴───────────────┘                    │
│                        │                                     │
│                   Single Agent                               │
│                   Single Deploy                              │
│                                                              │
│   ✅ Simple decorators                                       │
│   ✅ Test locally first                                      │
│   ✅ One deployment                                          │
│   ✅ Works with any model                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Why AWS AgentCore?

**AgentCore** is AWS's new serverless runtime specifically designed for AI agents:

### AgentCore vs Traditional Hosting

| Feature | EC2/ECS/Lambda | AgentCore |
|---------|----------------|-----------|
| **Cold Start** | Seconds | Milliseconds (microVMs) |
| **Scaling** | Manual/Config | Automatic |
| **Auth** | Build it yourself | Built-in OAuth/JWT |
| **Logging** | CloudWatch setup | Automatic |
| **Cost** | Pay for idle | Pay per invocation |

### How AgentCore Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Development                          │
│                                                              │
│   handler.py + tools + requirements.txt                     │
│                        │                                     │
│                        ▼                                     │
│              agentcore configure                             │
│         (generates Dockerfile, buildspec)                    │
│                        │                                     │
│                        ▼                                     │
│               agentcore deploy                               │
│         (CodeBuild → ECR → AgentCore)                       │
│                        │                                     │
│                        ▼                                     │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                AWS AgentCore Runtime                         │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Firecracker │  │  Firecracker │  │  Firecracker │        │
│  │   microVM    │  │   microVM    │  │   microVM    │        │
│  │  (your agent)│  │  (your agent)│  │  (your agent)│        │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │               │               │                    │
│         └───────────────┴───────────────┘                   │
│                         │                                    │
│              Auto-scaling, built-in auth                    │
│              Millisecond cold starts                        │
└─────────────────────────────────────────────────────────────┘
```

**AgentCore microVMs** boot in milliseconds (not seconds like Lambda) because they use Firecracker - the same technology behind Lambda but optimized for long-running agent conversations.

---

## AgentCore: Production-Ready Agent Platform

Amazon Bedrock AgentCore is a **modular set of capabilities** to build, deploy, and operate production-grade agents securely and scalably using **any framework and any model**.

### AgentCore Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Agent                                       │
│              Any framework, any model, all popular protocols             │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
           Build             Deploy            Assess
              │                 │                 │
              ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      AgentCore Native Resources                          │
│                                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Memory  │ │ Built-in │ │ Gateways │ │ Identity │ │  Policy  │      │
│  │          │ │  Tools   │ │          │ │          │ │          │      │
│  │ Short &  │ │  Code    │ │  APIs,   │ │ Inbound  │ │  Auth    │      │
│  │ Long-term│ │Interpret,│ │ Lambda   │ │ Outbound │ │ Control  │      │
│  │ memory   │ │ Browser  │ │functions │ │  Auth    │ │          │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│                                                                          │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────┐      │
│  │    Observability     │  │     Evaluations      │  │ Runtime  │      │
│  │  Monitor and debug   │  │ Pre-built & custom   │  │ Agents,  │      │
│  │                      │  │    evaluators        │  │  tools   │      │
│  └──────────────────────┘  └──────────────────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
```

### AgentCore Capabilities Explained

| Capability | What It Does | Why It Matters |
|------------|--------------|----------------|
| **Runtime** | Secure, serverless execution for agents and tools | Fast cold starts, session isolation, multi-modal support |
| **Memory** | Short & long-term memory across sessions | Agents learn and retain context continuously |
| **Built-in Tools** | Code interpreter, Browser | Production-ready tools without building from scratch |
| **Gateways** | MCP, OpenAPI, REST API schemas | Call tools via standard protocols, no custom code |
| **Identity** | Inbound & outbound authentication | Secure access control with OAuth/JWT providers |
| **Policy** | Authorization control using Cedar | Define exactly what agents can do under what conditions |
| **Observability** | Monitor and debug agents | Production visibility into agent behavior |
| **Evaluations** | Pre-built and custom evaluators | Assess agent quality before and after deployment |

### Runtime: The Core of AgentCore

The **Runtime** is purpose-built for AI agents:

- **Fast cold starts** - Millisecond startup using Firecracker microVMs
- **Long-running execution** - Support for extended agent conversations
- **True session isolation** - Each invocation runs in its own secure environment
- **Built-in Identity** - Authentication handled at the platform level
- **Multi-modal payloads** - Support for images, documents, and other content
- **Framework agnostic** - Works with Strands, LangChain, or any framework

### Policy: Guardrails for What Agents Can DO

The **Policy** capability provides deterministic control over agent actions:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AgentCore Policy Layer                        │
│                                                                  │
│   Uses Cedar (AWS's open-source policy language) to define:     │
│                                                                  │
│   • WHO can invoke the agent                                     │
│   • WHAT tools the agent can use                                 │
│   • WHEN actions are allowed (time-based rules)                  │
│   • WHICH resources tools can access                             │
│   • HOW much data can be processed                               │
│                                                                  │
│   Example Cedar Policy:                                          │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ permit(                                                  │   │
│   │   principal == User::"devops-team",                      │   │
│   │   action == Action::"invoke-tool",                       │   │
│   │   resource == Tool::"deploy-to-production"               │   │
│   │ ) when {                                                 │   │
│   │   context.time.hour >= 9 && context.time.hour <= 17      │   │
│   │ };                                                       │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Key difference**:
- **Guardrails** control what the LLM can *say* (content filtering)
- **Policy** controls what tools can *do* (action authorization)

### Identity: Secure Access Control

AgentCore Identity integrates with leading identity providers:

| Direction | What It Does | Use Case |
|-----------|--------------|----------|
| **Inbound Identity** | Authenticate callers to your agent | Verify users before allowing agent access |
| **Outbound Identity** | Provide credentials to downstream resources | Agent securely accesses APIs, databases |

This lab demonstrates inbound identity with **Amazon Cognito** (Steps 7a & 7b).

### Gateways: Universal Tool Access

Gateways support multiple protocols for connecting agents to tools:

- **MCP (Model Context Protocol)** - Open standard for AI tools
- **OpenAPI schemas** - Connect to any REST API
- **Lambda functions** - Custom serverless tools
- **Pre-configured integrations** - AWS services, common SaaS tools

No custom code required - just configure and connect.

### Why AgentCore is AWS's Flagship Agent Platform

AWS is positioning AgentCore as the **primary platform for production AI agents**, consolidating capabilities that were previously fragmented:

| Before (Bedrock Agents) | After (AgentCore) |
|------------------------|-------------------|
| Lambda for each tool | Single runtime for agent + tools |
| Manual IAM per function | Unified identity layer |
| No built-in memory | Short & long-term memory |
| Custom observability | Built-in monitoring |
| Basic guardrails | Policy + Guardrails + Evaluations |
| Framework-specific | Framework agnostic |

**Bottom line**: AgentCore is designed from the ground up for production agent workloads, while Bedrock Agents was an evolution of Lambda-based orchestration.

---

## MCP: The Universal Tool Protocol

**Model Context Protocol (MCP)** is an open standard for connecting AI to external tools.

### Why MCP Matters

Without MCP, every AI framework has its own tool format:
- LangChain tools
- OpenAI function calling
- Bedrock Agent actions
- Custom implementations

**MCP standardizes this** - write a tool once, use it anywhere.

### MCP in This Lab

We use MCP to connect to external tool servers:

```python
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Connect to any MCP server
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx",
        args=["mcp-server-fetch"]  # Web fetching MCP server
    )
))

with mcp_client:
    tools = mcp_client.list_tools_sync()
    # Now your agent can fetch any URL!
```

### MCP vs Direct Integration

| Approach | Pros | Cons |
|----------|------|------|
| **Direct API calls** | Simple, no dependencies | Tight coupling, rewrite for each agent |
| **MCP servers** | Reusable, standardized | Extra abstraction layer |

**This lab uses both:**
- **Direct tools** (`@tool`) for simple integrations (weather, AWS status, IPAM)
- **MCP** for standardized external tools (web fetching)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     DevOps Decision Agent                        │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │  Weather   │  │ AWS Status │  │   IPAM     │  │    MCP     │ │
│  │   Tool     │  │   Tool     │  │   Tool     │  │   Tools    │ │
│  │  @tool     │  │  @tool     │  │  @tool     │  │  External  │ │
│  │            │  │            │  │ (Infoblox) │  │  Servers   │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
│        │               │               │               │         │
│        └───────────────┴───────────────┴───────────────┘         │
│                                │                                  │
│                    ┌───────────▼───────────┐                     │
│                    │    System Prompt      │                     │
│                    │  "You are a DevOps    │                     │
│                    │   Decision Agent..."  │                     │
│                    └───────────┬───────────┘                     │
│                                │                                  │
│                    ┌───────────▼───────────┐                     │
│                    │   Claude 3.5 Sonnet   │                     │
│                    │   (via Bedrock)       │                     │
│                    └───────────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS Bedrock AgentCore                         │
│                                                                  │
│   • Serverless microVM hosting (Firecracker)                    │
│   • Auto-scaling based on demand                                │
│   • Built-in authentication (OAuth 2.0)                         │
│   • Automatic logging and monitoring                            │
│   • Pay-per-invocation pricing                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  OAuth 2.0 Security Layer                        │
│                                                                  │
│   ┌─────────────┐         ┌─────────────┐                       │
│   │  Cognito    │◀────────│   Agent     │                       │
│   │  User Pool  │ Token   │   Client    │                       │
│   └─────────────┘         └─────────────┘                       │
│         │                                                        │
│         │ Validates JWT                                          │
│         ▼                                                        │
│   ┌─────────────┐         ┌─────────────┐                       │
│   │  AgentCore  │────────▶│   Tools     │                       │
│   │  Gateway    │ Secure  │   (Lambda)  │                       │
│   └─────────────┘         └─────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Lab Steps

### Step 1: Hello World Agent
Create your first agent with Strands SDK and Bedrock.
```bash
python lab/exercises/step1_hello_agent.py
python lab/tests/test_step1.py
```

### Step 2: Weather Tool
Build a custom `@tool` that fetches weather data.
```bash
python lab/exercises/step2_weather_tool.py
python lab/tests/test_step2.py
```

### Step 3: AWS Status Tool
Create a tool that checks AWS service health.
```bash
python lab/exercises/step3_aws_status_tool.py
python lab/tests/test_step3.py
```

### Step 3b: IPAM Tool (Infoblox CSP)
Build enterprise integration with Infoblox for IP capacity checks.
```bash
# Optional: export IPAM_API_KEY=your_key (uses mock data without it)
python lab/exercises/step3b_ipam_tool.py
python lab/tests/test_step3b.py
```

### Step 4: MCP Integration
Connect to external MCP tool servers.
```bash
python lab/exercises/step4_mcp_integration.py
python lab/tests/test_step4.py
```

### Step 5: System Prompt Design
Craft the agent's personality and response format.
```bash
python lab/exercises/step5_system_prompt.py
python lab/tests/test_step5.py
```

### Step 6: Deploy to AgentCore
Package and deploy your agent to AWS.
```bash
python lab/exercises/step6_agentcore_handler.py
python lab/tests/test_step6.py

# Deploy to cloud
agentcore configure -e lab/exercises/step6_agentcore_handler.py -r us-west-2 --disable-memory -n devops_agent
agentcore deploy
agentcore invoke '{"prompt": "Should I deploy to us-east-1?"}'
```

### Step 7a: Cognito OAuth Setup
Learn OAuth 2.0 by creating a Cognito User Pool.
```bash
python lab/exercises/step7a_cognito_oauth.py
python lab/tests/test_step7a.py
```

### Step 7b: Gateway Authentication
Secure your agent with JWT authentication.
```bash
python lab/exercises/step7b_gateway_auth.py
python lab/tests/test_step7b.py
```

---

## Prerequisites

- Python 3.10+
- AWS account with Bedrock access (Claude models enabled)
- AWS CLI configured
- uv/uvx installed (for MCP): `pip install uv`
- (Optional) Infoblox CSP API key

## Quick Start

```bash
git clone https://github.com/iracic82/AWS_AgentLab.git
cd AWS_AgentLab
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the lab!
python lab/exercises/step1_hello_agent.py
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AWS_PROFILE` | AWS CLI profile | If not default |
| `AWS_REGION` | AWS region | No (defaults to us-west-2) |
| `IPAM_API_KEY` | Infoblox CSP API key | No (uses mock data) |

## Cleanup

```bash
agentcore destroy
python lab/exercises/step7b_gateway_auth.py --cleanup
python lab/exercises/step7a_cognito_oauth.py --cleanup
```

---

## Key Takeaways

After completing this lab, you'll understand:

1. **Strands Agents SDK** - The simplest way to build production AI agents
2. **Tool Design** - How to create tools agents can use effectively
3. **MCP** - The universal protocol for AI-tool integration
4. **AgentCore** - Serverless hosting designed for AI agents
5. **OAuth 2.0** - Securing agent APIs in production

## Resources

- [Strands Agents SDK](https://github.com/strands-agents/strands)
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Infoblox CSP API](https://docs.infoblox.com/)
