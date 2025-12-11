# Step 6: Deploy to AgentCore

This step deploys our DevOps Decision Agent to AWS AgentCore Runtime.

## Prerequisites

1. AWS credentials configured
2. AgentCore toolkit installed:
   ```bash
   pip install bedrock-agentcore-starter-toolkit
   ```

## Deployment Commands

### 1. Configure the deployment
```bash
cd /Users/iracic/PycharmProjects/AWS_AgentLab
agentcore configure -e handler.py
```

This creates `.bedrock_agentcore.yaml` with your deployment settings.

Options:
- Add `-r us-east-1` to change region (default: us-west-2)
- Add `--disable-memory` to skip memory provisioning

### 2. Deploy to AgentCore
```bash
agentcore deploy
```

This will:
- Package your Python code
- Create AWS resources (S3, IAM roles)
- Deploy to AgentCore Runtime
- Return the Agent ARN (save this!)

### 3. Test the deployed agent
```bash
agentcore invoke '{"prompt": "Should I deploy my app to us-east-1 today?"}'
```

### 4. Check status
```bash
agentcore status
```

### 5. View logs
```bash
agentcore logs
```

## Cleanup

When done testing:
```bash
agentcore destroy
```

## What AgentCore Handles

- **No Docker required** - Uses direct code deployment
- **Auto-scaling** - Serverless microVMs managed by AWS
- **Logging/Tracing** - Built-in observability
- **Auth** - AgentCore Identity for secure access

## Next Steps

After successful deployment:
1. Test with various prompts
2. Check CloudWatch logs
3. Integrate with AgentCore Identity for auth (see Step 7)
