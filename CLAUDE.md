# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DevOps Decision Agent Lab - training material for building AI agents with Strands SDK, MCP, and AWS AgentCore.

## Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run steps
python steps/step1_hello_agent.py   # Basic agent
python steps/step2_weather_tool.py  # With weather tool
python steps/step3_aws_status_tool.py  # With AWS status
python steps/step4_mcp_integration.py  # With MCP
python steps/step5_complete_agent.py   # Interactive mode

# AgentCore deployment
agentcore configure -e handler.py
agentcore deploy
agentcore invoke '{"prompt": "test"}'
agentcore destroy
```

## Architecture

- `src/tools/` - Custom tools using `@tool` decorator
- `src/agent.py` - Main agent combining tools + MCP
- `handler.py` - AgentCore entry point with `@app.entrypoint`
- `steps/` - Incremental lab exercises

## Key Patterns

Custom tool:
```python
from strands.tools import tool

@tool
def my_tool(param: str) -> dict:
    """Tool description for the LLM."""
    return {"result": "value"}
```

MCP integration requires context manager:
```python
with mcp_client:
    tools = mcp_client.list_tools_sync()
    agent = Agent(tools=tools)
```
